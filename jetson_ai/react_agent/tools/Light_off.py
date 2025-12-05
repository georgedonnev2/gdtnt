from react_agent.toolBase import BaseTool, register_tool
import Jetson.GPIO as GPIO
import time

# 编写工具类
@register_tool('light_off')
class LightOff(BaseTool):
    description = 'This tool can be used to turn off the light.'
    parameters = [{}]
    requirement='该工具无需传递参数'

    def call(self, **kwargs) -> str:
        led_pin = 7
        GPIO.setmode(GPIO.BOARD)
        #设置led_pin引脚为输出模式。
        GPIO.setup(led_pin, GPIO.OUT)

        for _ in range(3):
            GPIO.output(led_pin, GPIO.LOW)
            time.sleep(1)
        GPIO.cleanup()
        return "灯已经成功关闭"