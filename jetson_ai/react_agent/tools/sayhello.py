from react_agent.toolBase import BaseTool, register_tool
import Jetson.GPIO as GPIO

# 编写工具类
@register_tool('sayhello')
class sayhello(BaseTool):
    description = "If the user says '和新朋友打个招呼', you must use this tool to greet new friends."
    parameters = [{}]
    requirement='该工具无需传递参数'

    def call(self, **kwargs) -> str:
        from rpi_TM1638 import TMBoards
        TM = TMBoards(stb=17, clk=27, dio=22)
        chs = "hello"
        for idx in range(len(chs)):
            TM.segments[idx] = chs[idx]
        GPIO.cleanup()
        return "成功打招呼"
