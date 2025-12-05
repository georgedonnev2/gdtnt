import gradio as gr
from agent_app.agent import init_agent
from utils.asr import asr
from utils.tts import tts
from utils.stats import led_manager

agent = init_agent()

# 定义聊天机器人的响应函数
def chatbot_response(user_input, history, messages):
    messages.append({'role': 'user', 'content': user_input})
    response = ""
    for chunk in agent.chat(messages):
        response += chunk
        yield history + [(user_input, response)], messages
    # 返回格式化后的历史记录
    messages.append({'role': 'assistant', 'content': response})
    return history + [(user_input, response)], messages

def audio_chat(audio, history, messages):
    user_input = asr(audio)
    messages.append({'role': 'user', 'content': user_input})
    response = ""
    for chunk in agent.chat(messages):
        response += chunk
        yield history + [(user_input, response)], messages
    # 返回格式化后的历史记录
    messages.append({'role': 'assistant', 'content': response})
    
    return history + [(user_input, response)], messages

def toSpeech(messages):
    result = messages[-1]['content'] \
        .replace("**Thought**", "") \
        .replace("**Action**", "") \
        .replace("**Action input**", "") \
        .replace("**Observation**", "") \
        .replace("**Final Answer**", "")
    audio = tts(result)
    return audio

# 使用 Gradio Blocks 构建聊天界面
with gr.Blocks() as demo:
    gr.Markdown("# 语音聊天机器人")
    messages = gr.State([])
    
    with gr.Row():
        chatbot = gr.Chatbot(label="agent", height=440)

    with gr.Row():
        with gr.Column():
            user_audio = gr.Audio(source="microphone", type="filepath", label="输入语音", optional=True)
        with gr.Column():
            output_audio = gr.Audio(show_download_button=False, label="输出语音", autoplay=True)
    
    with gr.Row():
        with gr.Column(scale=10):
            user_input = gr.Textbox(placeholder="输入你的消息（Enter发送）", label="文本输入")
        with gr.Column(scale=2):
            reset_btn = gr.Button('重置状态(首次对话前执行)')

    # 提交输入时更新聊天记录
    user_input.submit(chatbot_response, [user_input, chatbot, messages], [chatbot, messages]) \
        .then(toSpeech, [messages], [output_audio]) \
        .then(lambda x:None, [], [user_input])
    user_audio.stop_recording(audio_chat, [user_audio, chatbot, messages], [chatbot, messages]) \
        .then(toSpeech, [messages], [output_audio])
    
    reset_btn.click(led_manager.reset, [], [])
    
# 启动应用
demo.queue().launch(server_name="0.0.0.0")
