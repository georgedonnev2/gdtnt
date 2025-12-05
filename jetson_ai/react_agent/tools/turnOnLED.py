from react_agent.toolBase import BaseTool, register_tool
import Jetson.GPIO as GPIO
from utils.stats import led_manager

# 编写工具类
@register_tool('LED_ON')
class LedOn(BaseTool):
    description = 'This tool can light up the corresponding LED lights by passing numbers.'
    parameters = [{
        'name': 'leds',
        'type': 'List',
        'description': 'led灯序号的列表，1<=序号<=8',
        'required': True
    }]
    requirement='该工具参数需要以dict对象方式传递'

    def call(self, leds, **kwargs) -> str:
        from rpi_TM1638 import TMBoards

        TM = TMBoards(stb=17, clk=27, dio=22)

        # 矫正状态
        temp = led_manager.get_stats()
        for idx in leds:
            temp[idx-1] = True
        led_manager.set_stats(temp)

        for idx in range(len(temp)):
            TM.leds[idx] = temp[idx]
        
        GPIO.cleanup()
        return "成功点亮Led灯"