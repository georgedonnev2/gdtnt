from react_agent.toolBase import BaseTool, register_tool
import Jetson.GPIO as GPIO
import time

# 编写工具类
@register_tool('get_day')
class GetDay(BaseTool):
    description = "This tool can get if it's day or night"
    parameters = [{}]
    requirement='该工具无需传递参数'

    def call(self, **kwargs) -> str:
        # 设置 GPIO 模式
        GPIO.setmode(GPIO.BCM)  # 使用 BCM 编号
        sensor_pin = 10  # 假设将 OUT 接到 GPIO 17

        # 设置引脚为输入模式
        GPIO.setup(sensor_pin, GPIO.IN)
        
        light_status = -1
        for _ in range(3):
            # 读取光敏电阻的数字信号
            light_status = GPIO.input(sensor_pin)
            time.sleep(1)  # 每秒读取一次
        
        GPIO.cleanup()
        if light_status == 1:
            return("状态: 1 (黑天)")
        else:
            return("状态: 0 (白天)")  # 输入为 0，表示白天