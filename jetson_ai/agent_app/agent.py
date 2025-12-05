from react_agent.LLM import RequestLLM
from react_agent.agent import ReactAgent
from react_agent.toolBase import tools_registry
from react_agent.tools import Light_off, Light_on, get_day, getTemperature, music_play, music_switch, music_stop, turnOnLED, turnOffLED, tubeON, sayhello

#from react_agent.tools import music_play, music_switch, music_stop
from config import *


def init_agent():
    # 1. 实例化agent
    llm = RequestLLM(base_url=LLM_URL, model_name=LLM_MODEL_NAME)
    agent = ReactAgent(llm)
    # 2. 注册工具
    for name, cls in tools_registry.items():
        agent.register_tool(name, cls)

    return agent
