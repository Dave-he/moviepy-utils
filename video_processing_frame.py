from moviepy import VideoFileClip, VideoClip
import numpy as np
from logutil import suppress_output
import time

def process_frame_with_context(clip, t):
    fps = clip.fps
    frame_index = int(t * fps)
    total_frames = int(clip.duration * fps)
    current_frame = clip.get_frame(t)

    # 收集当前帧以及前后各 4 帧
    frames = []
    for i in range(frame_index - 4, frame_index + 5):
        if 0 <= i < total_frames:
            frame = clip.get_frame(i / fps)
        else:
            # 如果超出边界，使用当前帧填充
            frame = current_frame
        frames.append(frame)

    # 获取单帧的宽度和高度
    height, width, _ = frames[0].shape

    # 创建一个空白的 9 宫格图像
    stitched_frame = np.zeros((height * 3, width * 3, 3), dtype=np.uint8)

    # 将 9 帧图像拼接到 9 宫格中
    for i in range(9):
        row = i // 3
        col = i % 3
        stitched_frame[row * height:(row + 1) * height, col * width:(col + 1) * width] = frames[i]

    return stitched_frame


@suppress_output
def process_video(input_video_path, output_video_path):
    try:
        # 打开视频文件
        clip = VideoFileClip(input_video_path)

        def make_frame(t):
            return process_frame_with_context(clip, t)

        # 创建新的视频剪辑
        new_clip = VideoClip(make_frame, duration=clip.duration)
        new_clip.fps = clip.fps

        # 逐帧写入新视频，添加 ffmpeg_params 参数
        new_clip.write_videofile(output_video_path, fps=clip.fps, threads=12, codec='libx264',
                                 ffmpeg_params=['-loglevel', 'quiet'])

        # 关闭视频剪辑对象
        clip.close()
        new_clip.close()
    except Exception as e:
        print(f"处理视频时出现错误: {e}")



if __name__ == "__main__":
    s = time.time()
    print(f"开始处理视频...{s}")
    for i in range(1, 4):
        s1 = time.time()
        input_video_path = f'input{i}.mp4'
        output_video_path = f'output{i}.mp4'
        process_video(input_video_path, output_video_path)
        print(f"已处理视频 {i}...耗时 {time.time() - s1:.2f} 秒")
        
    print(f"视频处理完成...总耗时 {time.time() - s:.2f} 秒")