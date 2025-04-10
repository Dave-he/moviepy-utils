# 视频工具箱moviepy-utils

本项目是基于python的moviepy实现视频工具集合，主要用于视频的剪辑、合成、转场等操作。

## 安装
'''
pip install moviepy
'''

## 功能
video_frame_stitching.py 将视频9帧拼接为一帧。（占用内存过大，建议使用video_processing_frame）
video_processing_frame.py 将视频将视频9帧拼接为一帧

video_merge.py 同目录下的视频拼接（按文件名排序）
video_transcode.py 视频转码
video_clip.py 视频裁剪