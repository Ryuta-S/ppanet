# coding=utf-8

# ===============================================
# Author: RyutaShitomi
# date: 2019-07-25T06:03:15.492Z
# Description:
#
# ===============================================

"""

"""
# packages
import tensorflow as tf
import os
import numpy as np
from tensorflow.contrib import slim

# user packages
from lib.models.backbone import feature_extractor

FLAGS = tf.app.flags.FLAGS

# DEFINE FLAGS
# tf.app.flags.DEFINE_string('dataset_dir',
#                            os.path.join('dataset', 'CamVid', 'tfrecord'),
#                            'tfrecord directory')

def build_model(images,
                num_classes,
                model_variant,
                output_stride=8,
                fine_tune_batch_norm=True,
                weight_decay=0.0001,
                backbone_atrous_rate=None,
                is_training=True,
                ppm_rates=[1, 2, 3, 6],
                ppm_pooling_type='average'):

    if backbone_atrous_rate is not None:
        if 'beta' not in model_variant:
            raise ValueError('{} is not correct.'.format(model_variant))
    _, images_height, images_width, _ = images.get_shape().as_list()
    features, end_points = feature_extractor.extract_features(
                           images=images,
                           output_stride=output_stride,
                           model_variant=model_variant,
                           weight_decay=weight_decay,
                           is_training=is_training,
                           fine_tune_batch_norm=fine_tune_batch_norm,
                           preprocess_images=True,
                           multi_grid=backbone_atrous_rate,
                           preprocessed_images_dtype=images.dtype,
                           )

    print('build_model')

    for key, val in end_points.items():
        print('{}: {}'.format(key, val.shape))

    print('features: {}, shape: {}'.format(features.name, features.get_shape().as_list()))

    if ppm_rates:

        # ppm_features = _build_PPM(is_training=is_training,
        #                           fine_tune_batch_norm=fine_tune_batch_norm,
        #                           ppm_rates)
        batch_norm_params = {
            'is_training': is_training and fine_tune_batch_norm,
            'decay': 0.9996,
            'epsilon': 1e-5,
            'scale': True
        }
        features_list = [features]
        _, base_height, base_width, _ = features.get_shape().as_list()
        with slim.arg_scope(
                [slim.conv2d],
                weights_regularizer=slim.l2_regularizer(weight_decay),
                weights_initializer=tf.truncated_normal_initializer(stddev=0.01),
                activation_fn=tf.nn.relu,
                normalizer_fn=slim.batch_norm,
                padding='SAME',
                stride=1):
            with slim.arg_scope([slim.batch_norm], **batch_norm_params):
                with tf.variable_scope('ppm', [features]):
                    for rate in ppm_rates:
                        kernel_height = int(base_height / rate)
                        kernel_width  = int(base_width  / rate)
                        pool_feature = slim.avg_pool2d(features, [kernel_height, kernel_width], stride=[kernel_height, kernel_width])
                        pool_feature = slim.conv2d(pool_feature, 256, 1, scope='kernel_{}'.format(rate))
                        print('============= rate {} ==============='.format(rate))
                        print('pool_feature.shape: {}'.format(pool_feature.get_shape().as_list()))
                        resized_feature = tf.image.resize_bilinear(pool_feature, [base_height, base_width], align_corners=True)
                        print('resized_feature.shape: {}'.format(resized_feature.get_shape().as_list()))
                        features_list.append(resized_feature)
                    ppm_feature = tf.concat(features_list, axis=3)
                ppm_feature = slim.conv2d(ppm_feature, 1024, 3)
                ppm_feature = slim.conv2d(ppm_feature, num_classes, 3)

    return tf.image.resize_bilinear(ppm_feature, [images_height, images_width], align_corners=True)
