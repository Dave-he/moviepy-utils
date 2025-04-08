from moviepy import VideoFileClip, VideoClip
import numpy as np

import logging
import os
# 设置 moviepy 的日志级别为 ERROR，只在出现错误时打印日志
logging.getLogger("moviepy").setLevel(logging.ERROR)
logging.getLogger("imageio").setLevel(logging.ERROR)
# 全局禁止 FFmpeg 日志（在脚本开头添加）
os.environ["IMAGEIO_FFMPEG_LOG_LEVEL"] = "error"  # 可选值：'debug', 'info', 'warn', 'error', 'quiet'

def process_frame_with_context(clip, t):
    fps = clip.fps
    frame_index = int(t * fps)
    total_frames = int(clip.duration * fps)

    # 收集当前帧以及前后各 4 帧
    frames = []
    for i in range(frame_index - 4, frame_index + 5):
        if 0 <= i < total_frames:
            frame = clip.get_frame(i / fps)
            frames.append(frame)
        else:
            # 如果超出边界，使用空白帧填充
            blank_frame = np.zeros_like(clip.get_frame(0))
            frames.append(blank_frame)

    # 这里可以对收集的 9 帧进行具体处理，示例中简单返回当前帧
    current_frame = frames[4]
    return current_frame


def process_video(input_video_path, output_video_path):
    try:
        # 打开视频文件
        clip = VideoFileClip(input_video_path)

        def make_frame(t):
            return process_frame_with_context(clip, t)

        # 创建新的视频剪辑
        new_clip = VideoClip(make_frame, duration=clip.duration)
        new_clip.fps = clip.fps

        # 逐帧写入新视频
        new_clip.write_videofile(output_video_path, fps=clip.fps,
            threads=12, codec='libx264',ffmpeg_params=['-loglevel', 'quiet'])

        # 关闭视频剪辑对象
        clip.close()
        new_clip.close()
    except Exception as e:
        print(f"处理视频时出现错误: {e}")


if __name__ == "__main__":
    for i in range(1, 3):
        input_video_path = f'input{i}.mp4'
        output_video_path = f'output{i}.mp4'
        process_video(input_video_path, output_video_path)
    