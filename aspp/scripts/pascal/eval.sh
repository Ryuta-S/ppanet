# coding=utf-8

# ===============================================
# Author: RyutaShitomi
# date: 2019-08-30T05:30:32.834Z
# Description:
#
# ===============================================

TRAIN_LOGDIR='aspp/logs/pascal/2019-11-17_train'

python eval.py \
       --output_stride=8 \
       --crop_size=512,512 \
       --batch_size=1 \
       --model_variant=resnet_v1_101_beta \
       --backbone_atrous_rates=1 \
       --backbone_atrous_rates=2 \
       --backbone_atrous_rates=4 \
       --decoder_output_stride=4 \
       --atrous_rates=12 \
       --atrous_rates=24 \
       --atrous_rates=36 \
       --module_order=aspp \
       --eval_logdir=${TRAIN_LOGDIR} \
       --checkpoint_dir=${TRAIN_LOGDIR} \
       --dataset_name=pascal \
       --dataset_dir=dataset/VOCdevkit/tfrecord \
       --split_name=val
