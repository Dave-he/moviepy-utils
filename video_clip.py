from moviepy import VideoFileClip

def clip_video(input_path, output_path, duration):
    """
    该函数用于截取视频的前几秒
    :param input_path: 输入视频的文件路径
    :param output_path: 输出视频的文件路径
    :param duration: 截取的时长（秒）
    """
    # 加载视频文件
    video = VideoFileClip(input_path)
    # 截取视频的前几秒
    new_video = video.subclip(0, duration)
    # 保存截取后的视频
    new_video.write_videofile(output_path, codec="libx264")
    # 关闭视频文件
    video.close()
    new_video.close()


if __name__ == "__main__":
    # 示例用法
    input_video = "input.mp4"
    output_video = "output.mp4"
    # 截取前 10 秒
    duration = 10
    clip_video(input_video, output_video, duration)
        