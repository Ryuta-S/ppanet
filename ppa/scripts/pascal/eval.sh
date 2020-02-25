# coding=utf-8

# ===============================================
# Author: RyutaShitomi
# date: 2019-08-30T05:30:32.834Z
# Description:
#
# ===============================================

MODULE_NAME='ppa'
DATASET='pascal'
MODEL_VARIANT='resnet_v1_101_beta'
TRAIN_LOGDIR='ppa/logs/'${DATASET}'/2019-11-30_train'
DATASET_DIR='./dataset/VOCdevkit/tfrecord'

python eval.py \
       --output_stride=8 \
       --batch_size=1 \
       --crop_size=512,512 \
       --model_variant=${MODEL_VARIANT} \
       --backbone_atrous_rates=1 \
       --backbone_atrous_rates=2 \
       --backbone_atrous_rates=4 \
       --decoder_output_stride=4 \
       --atrous_rates=12 \
       --atrous_rates=24 \
       --atrous_rates=36 \
       --ppm_rates=1 \
       --ppm_rates=2 \
       --ppm_rates=3 \
       --ppm_rates=6 \
       --ppm_pooling_type=avg \
       --module_order=ppa \
       --eval_logdir=${TRAIN_LOGDIR} \
       --checkpoint_dir=${TRAIN_LOGDIR} \
       --split_name=val \
       --dataset_name=${DATASET} \
       --dataset_dir=${DATASET_DIR}
