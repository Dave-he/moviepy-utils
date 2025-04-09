import os
from moviepy import VideoFileClip
from logutil import suppress_output

@suppress_output
def transcode_video(input_path, output_path, codec='libx264', resolution=None, fps=None):
    """
    转码视频文件，并可调整分辨率和帧率
 
    :param input_path: 输入视频文件路径
    :param output_path: 输出视频文件路径
    :param codec: 编解码器，例如 'libx264' (H.264)，'libx265' (H.265)
    :param resolution: 分辨率，例如 (1280, 720)
    :param fps: 帧率，例如 24
    """
    # 读取视频文件
    video = VideoFileClip(input_path)
    
    # 设置帧率
    if fps is not None:
        video = video.set_fps(fps)
    
    # 设置分辨率
    if resolution is not None:
        video = video.resized(resolution)
    
    # 构建输出文件路径
    output_filename = os.path.splitext(os.path.basename(input_path))[0] + ".mp4"
    output_file_path = os.path.join(os.path.dirname(output_path), output_filename)
    
    # 转码并保存视频
    video.write_videofile(output_file_path, codec=codec)
    
    # 释放资源
    video.close()
 
if __name__ == "__main__":
    # 输入视频文件路径
    input_video_path = "input1.mp4"
    
    # 输出视频文件路径
    output_video_path = "output.mp4"
    
    # 调用转码函数
    transcode_video(input_video_path, output_video_path, codec='libx264', resolution=(640, 480), fps=None)
    
    print("视频转码完成")