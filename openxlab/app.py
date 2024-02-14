# 导入所需的库
from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig
import torch
import streamlit as st

from modelscope import snapshot_download

meta_instruction = ('你是唐三藏，原名陈玄奘，后因皈依佛教而改名。'
                    '你性格温和、仁慈，对徒弟们既严格又有爱心。他对佛法有着坚定的信仰，你的说话方式体现了学识和修养。你讲话通常文雅、有礼，使用的是较为正式和书面化的语言。作为一位高僧，你的话语中常带有佛学智慧，以及对人生和宇宙的深刻理解。'
                    '尽量保持回答的自然回答，当然你也可以适当穿插一些文言文，另外，书生·浦语是你的好朋友，是你的AI助手。')
# 在侧边栏中创建一个标题和一个链接
with st.sidebar:
    st.markdown("## InternLM LLM")
    "[InternLM](https://github.com/InternLM/InternLM)"
    "[XTuner](https://github.com/InternLM/xtuner)"
    "[三藏-Chat](https://github.com/JimmyMa99/SanZang-Chat)"
    "[八戒-Chat](https://github.com/JimmyMa99/BaJie-Chat)"
    "[悟空-Chat](https://github.com/JimmyMa99/WuKong-Chat)"
    "[悟净-Chat](https://github.com/JimmyMa99/WuJing-Chat)"
    # 创建一个滑块，用于选择最大长度，范围在0到1024之间，默认值为512
    max_length = st.slider("max_length", 0, 1024, 512, step=1)
    system_prompt = st.text_input("System_Prompt", meta_instruction)

# 创建一个标题和一个副标题
st.title("🪷 三藏-Chat Internlm2")
st.caption("🚀 A streamlit chatbot powered by InternLM2 QLora")

# 定义模型路径

model_id = 'JimmyMa99/SanZang-Chat'

mode_name_or_path = snapshot_download(model_id, revision='master')
# mode_name_or_path='process_data/merged_models/zbj'


# 定义一个函数，用于获取模型和tokenizer
@st.cache_resource
def get_model():
    # 从预训练的模型中获取tokenizer
    tokenizer = AutoTokenizer.from_pretrained(mode_name_or_path, trust_remote_code=True)
    # 从预训练的模型中获取模型，并设置模型参数
    model = AutoModelForCausalLM.from_pretrained(mode_name_or_path, trust_remote_code=True, torch_dtype=torch.bfloat16).cuda()
    model.eval()  
    return tokenizer, model

# 加载model和tokenizer
tokenizer, model = get_model()

# 如果session_state中没有"messages"，则创建一个包含默认消息的列表
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# 遍历session_state中的所有消息，并显示在聊天界面上
for msg in st.session_state.messages:
    st.chat_message("user").write(msg[0])
    st.chat_message("assistant").write(msg[1])

# 如果用户在聊天输入框中输入了内容，则执行以下操作
if prompt := st.chat_input():
    # 在聊天界面上显示用户的输入
    st.chat_message("user").write(prompt)
    # 构建输入     
    response, history = model.chat(tokenizer, prompt, meta_instruction=system_prompt, history=st.session_state.messages)
    # 将模型的输出添加到session_state中的messages列表中
    st.session_state.messages.append((prompt, response))
    # 在聊天界面上显示模型的输出
    st.chat_message("assistant").write(response)