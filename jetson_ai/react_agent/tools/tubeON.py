from react_agent.toolBase import BaseTool, register_tool
import Jetson.GPIO as GPIO

# 编写工具类
@register_tool('Tube_On')
class TubeOn(BaseTool):
    description = 'This tool can be used to displays letters and numbers on a digital tube.'
    parameters = [{
        'name': 'chs',
        'type': 'list',
        'description': '传入需要显示的字符串，字符串长度<=8',
        'required': True
    }]
    requirement='该工具参数需要以dict对象方式传递'

    def call(self, chs, **kwargs) -> str:
        from rpi_TM1638 import TMBoards
        TM = TMBoards(stb=17, clk=27, dio=22)
        for idx in range(len(chs)):
            TM.segments[idx] = chs[idx]
        GPIO.cleanup()
        return "成功显示对应字符"