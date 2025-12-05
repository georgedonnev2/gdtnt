from react_agent.toolBase import BaseTool, register_tool
import Jetson.GPIO as GPIO

# 编写工具类
@register_tool('Tube_Clear')
class TubeClear(BaseTool):
    description = 'This tool can be used to clear the display and the digits.'
    parameters = [{}]
    requirement='该工具无需传递'

    def call(self, leds, **kwargs) -> str:
        from rpi_TM1638 import TMBoards
        TM = TMBoards(stb=17, clk=27, dio=22)
        TM.clearDisplay()
        GPIO.cleanup()
        return "成功清空数码管状态"