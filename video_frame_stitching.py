import cv2
import numpy as np
from moviepy import VideoFileClip, ImageSequenceClip


def stitch_frames(frames):
    """
    将9帧图像拼接成一张图像
    :param frames: 9帧图像列表
    :return: 拼接后的图像
    """
    # 假设所有帧的尺寸相同
    height, width, _ = frames[0].shape
    # 创建一个新的空白图像，用于存储拼接后的图像
    stitched_image = np.zeros((3 * height, 3 * width, 3), dtype=np.uint8)
    # 按3x3的网格拼接图像
    for i in range(3):
        for j in range(3):
            index = i * 3 + j
            stitched_image[i * height:(i + 1) * height, j * width:(j + 1) * width] = frames[index]
    return stitched_image


def process_video(input_path, output_path):
    """
    处理视频，将每一帧替换为前4帧+本帧+后4帧拼接的图像~
    :param input_path: 输入视频的路径
    :param output_path: 输出视频的路径
    """
    # 打开视频文件
    clip = VideoFileClip(input_path)
    fps = clip.fps
    frames = []
    # 读取视频的每一帧
    for frame in clip.iter_frames():
        frames.append(frame)
    num_frames = len(frames)
    new_frames = []
    # 处理每一帧
    for i in range(num_frames):
        start = max(0, i - 4)
        end = min(num_frames, i + 5)
        # 补齐到9帧
        current_frames = frames[start:end]
        while len(current_frames) < 9:
            if len(current_frames) < i + 1:
                current_frames.insert(0, frames[0])
            else:
                current_frames.append(frames[-1])
        # 拼接9帧图像
        stitched_frame = stitch_frames(current_frames)
        new_frames.append(stitched_frame)
    # 创建新的视频剪辑
    new_clip = ImageSequenceClip(new_frames, fps=fps)
    # 保存新的视频
    new_clip.write_videofile(output_path, fps=fps)


if __name__ == "__main__":
    input_video_path = "input.mp4"
    output_video_path = "output.mp4"
    process_video(input_video_path, output_video_path)
    