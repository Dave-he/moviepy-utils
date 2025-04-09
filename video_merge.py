from moviepy import *
import os
import argparse
import re
from logutil import suppress_output

@suppress_output
def concatenate_videos(video_files, args):
    """拼接视频，在中间插入风格一致的转场封面并添加文字说明"""
    logs = []
    clips = []
    for idx, file in enumerate(video_files):
        current_clip = VideoFileClip(os.path.join(args.input_folder, file))
        
        # 保存原始参数
        original_size = current_clip.size
        original_fps = current_clip.fps
        original_duration = current_clip.duration

        # 调整分辨率
        if args.target_width:
            current_clip = current_clip.resized(width=args.target_width)
        
        # 打印参数
        logs.append(f"{file:<20} | {f'{original_size[0]}x{original_size[1]}':<10} | "
              f"{f'{current_clip.size[0]}x{current_clip.size[1]}':<10} | "
              f"{original_fps:<5.1f} | {original_duration:.2f}秒")

        # 处理转场
        durition = 3
        if args.transition_durition :
              durition =  args.transition_durition

        transition = None
        if (args.no_transition is None) :     
            if idx < len(video_files) - 1 and args.transition_clip and args.no_transition:
                transition_src = VideoFileClip(os.path.join(args.input_folder, args.transition_clip)).resized(width=args.target_width)
                transition = transition_src.set_duration(durition)
              
            else : 
                transition = create_transition_cover(current_clip.size,durition, idx)
            clips.extend([current_clip, transition])
        else:
            clips.append(current_clip)

    final_clip = concatenate_videoclips(clips, method="compose")
    return logs, final_clip


# 自定义排序函数，用于从文件名中提取数字部分
def extract_number(filename):
    numbers = re.findall(r'\d+', filename)
    if numbers:
        return int(numbers[0])
    return 0


def create_transition_cover(size, text, duration = 3, fontsize=50, color='white', bg_color=(0, 0, 0)):
    """创建通用风格的转场封面"""
    # 创建背景颜色剪辑
    bg_clip = ColorClip(size, color=bg_color, duration=duration)

    # 添加集数文本
    text_clip = TextClip(text, fontsize=fontsize, color=color)
    text_clip = text_clip.pos(('center', 'center')).set_duration(duration)

    # 合成背景和文本
    transition_cover = CompositeVideoClip([bg_clip, text_clip])
    return transition_cover



def main(path = "."):
    default_path = os.path.expanduser(path)
    default_out = default_path.split('/')[-1]+".mp4"
    print(f'{default_path}  out: {default_out}')
    parser = argparse.ArgumentParser(description='视频合并工具')
    parser.add_argument('--input-folder',  default=default_path, help='输入视频文件夹路径')
    parser.add_argument('--output-file', default=default_out.split('/')[-1], help='输出视频文件名')
    parser.add_argument('--transition-clip', default=None, help='转场视频文件名（默认：无）')
    parser.add_argument('--target-width', type=int, default=480, help='目标宽度（保持高宽比，默认：1280）')
    parser.add_argument('--bitrate', default="2000k", help='视频码率（默认：2000k）')
    parser.add_argument('--fps', type=int, default=None, help='输出帧率（默认：保持第一个视频的帧率）')
    parser.add_argument('--transition_durition', type=int, default=3, help='转场时长（默认：3秒）')
    parser.add_argument('--no-transition', type=bool, default=False, help='禁用转场效果')
    args = parser.parse_args()

    if not os.path.isdir(args.input_folder):
        print(f"错误：输入文件夹不存在 '{args.input_folder}'")
        return

    if args.transition_clip and not os.path.exists(os.path.join(args.input_folder, args.transition_clip)):
        print(f"警告：转场文件 '{args.transition_clip}' 不存在，将跳过转场")
        args.transition_clip = None

    video_files = sorted([
        f for f in os.listdir(args.input_folder)
        if f.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))
    ], key=extract_number)

    if not video_files:
        print("错误：未找到任何视频文件")
        return

    logs, final_clip= concatenate_videos(video_files, args)
  
    # 打印处理信息表头
    print("\n视频处理详情：")
    print("="*100)
    print(f"{'文件名':<20} | {'原始分辨率':<10} | {'调整后分辨率':<10} | {'帧率':<5} | {'时长':<8}")
    print("-"*100)
    for log in logs:
        print(log)

    print("-"*100)

    final_clip.write_videofile(
        args.output_file,
        args.fps,
        codec="libx264",
        audio_codec="aac",
        bitrate=args.bitrate,
        temp_audiofile="temp-audio.m4a",
        remove_temp=True
    )

    print("\n合并完成信息：")
    print("="*50)
    print(f"输出文件：{args.output_file}")
    print(f"总视频数：{len(video_files)}")
    print(f"最终分辨率：{final_clip.size[0]}x{final_clip.size[1]}")
    print(f"最终帧率：{final_clip.fps}fps")
    print(f"文件大小：{os.path.getsize(args.output_file) / 1024:.2f} KB")


#python video_merge.py --input-folder ./videos --output-file merged.mp4 > process.log
if __name__ == "__main__":
    main()
