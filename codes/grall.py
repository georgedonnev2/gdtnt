import gradio as gr
import numpy as np
import soundfile as sf
import shutil
import os

# 固定的文件名
FIXED_FLAC_FILE = "current_recording.flac"
TARGET_FLAC_FILE = "Recording.flac"


def save_and_process_audio(audio):
    """录音完成后自动保存为FLAC文件"""
    if audio is None:
        return "❌ 未检测到音频输入", None

    sample_rate, audio_data = audio

    try:
        # 保存为固定FLAC文件（覆盖模式）
        sf.write(
            file=FIXED_FLAC_FILE,
            data=audio_data,
            samplerate=sample_rate,
            format="FLAC",
            subtype="PCM_16",
        )

        duration = len(audio_data) / sample_rate
        message = f"✅ 录音已保存: {FIXED_FLAC_FILE}\n时长: {duration:.1f}秒, 采样率: {sample_rate}Hz"

        return message, FIXED_FLAC_FILE
    except Exception as e:
        return f"❌ 保存失败: {str(e)}", None


def copy_to_recording():
    """复制文件到当前目录的Recording.flac"""
    if not os.path.exists(FIXED_FLAC_FILE):
        return f"❌ 找不到 {FIXED_FLAC_FILE}，请先录制音频"

    try:
        # 复制文件
        shutil.copy2(FIXED_FLAC_FILE, TARGET_FLAC_FILE)

        # 验证复制结果
        if os.path.exists(TARGET_FLAC_FILE):
            file_size = os.path.getsize(TARGET_FLAC_FILE) / 1024
            return f"✅ 复制成功: {TARGET_FLAC_FILE} ({file_size:.1f}KB)"
        else:
            return "❌ 复制失败：目标文件未创建"
    except Exception as e:
        return f"❌ 复制失败: {str(e)}"


# 创建精简界面
with gr.Blocks(title="Jetson FLAC录音器", theme=gr.themes.Soft()) as demo:
    gr.Markdown("## 🎤 Jetson FLAC录音器")
    gr.Markdown("点击下方录音按钮开始/停止录音，录音将自动保存")

    # 录音组件
    audio_input = gr.Audio(
        sources="microphone",
        type="numpy",
        label="录音控制",
        format="wav",
        interactive=True,
    )

    # 状态显示
    status_display = gr.Textbox(label="状态", value="等待录音...", lines=2)

    # 播放界面（录音完成后自动显示）
    gr.Markdown("### 录音播放")
    audio_output = gr.Audio(label="最新录音", type="filepath", interactive=False)

    # 操作按钮
    gr.Markdown("### 文件操作")
    copy_button = gr.Button(
        "📁 执行指令：复制到Recording.flac", variant="primary", size="lg"
    )

    # 设置事件处理
    # 录音完成后自动保存并更新状态
    audio_input.change(
        fn=save_and_process_audio,
        inputs=[audio_input],
        outputs=[status_display, audio_output],
    )

    # 复制按钮
    copy_button.click(fn=copy_to_recording, inputs=None, outputs=[status_display])

# 启动应用
if __name__ == "__main__":
    print("启动Jetson FLAC录音器...")
    print(f"录音文件: {FIXED_FLAC_FILE}")
    print(f"目标文件: {TARGET_FLAC_FILE}")

    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
