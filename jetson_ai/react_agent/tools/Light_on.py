from react_agent.toolBase import BaseTool, register_tool
import Jetson.GPIO as GPIO
from utils.stats import led_manager

# 编写工具类
@register_tool('light_open')
class LightOn(BaseTool):
    description = 'This tool can be used to turn on the light.'
    parameters = [{}]
    requirement='该工具无需传递参数'

    def call(self, **kwargs) -> str:
        from rpi_TM1638 import TMBoards
        TM = TMBoards(stb=17, clk=27, dio=22)

        # 矫正状态
        temp = led_manager.get_stats()
        for idx in range(len(temp)):
            TM.leds[idx] = True
            temp[idx] = True
        led_manager.set_stats(temp)

        GPIO.cleanup()
        return "灯已经成功打开"