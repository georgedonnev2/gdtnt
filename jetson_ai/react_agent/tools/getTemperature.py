from react_agent.toolBase import BaseTool, register_tool
from smbus2 import SMBus, i2c_msg
import time

# 初始化 I2C 总线
I2C_BUS = 7  # Jetson Nano 上通常使用 I2C 总线 1
DHT20_ADDRESS = 0x38  # DHT20 默认 I2C 地址

bus = SMBus(I2C_BUS)

def init_dht20():
    global bus
    # 发送初始化命令
    msg = i2c_msg.write(DHT20_ADDRESS, [0xBE, 0x08, 0x00])
    bus.i2c_rdwr(msg)
    time.sleep(0.02)  # 等待传感器准备好

def read_dht20():
    global bus
    msg = i2c_msg.write(DHT20_ADDRESS, [0xAC, 0x33, 0x00])
    bus.i2c_rdwr(msg)


    # 读取 7 字节的数据
    msg = i2c_msg.read(DHT20_ADDRESS, 7)
    bus.i2c_rdwr(msg)
    data = []
    for k in range(msg.len):
        data.append(ord(msg.buf[k]))

    # 处理读取的数据
    humidity_raw = (data[1] << 12) | (data[2] << 4) | (data[3] >> 4)
    temperature_raw = ((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]

    # 转换为实际温度和湿度值
    humidity = (humidity_raw / 1048576.0) * 100
    temperature = (temperature_raw / 1048576.0) * 200 - 50

    return temperature, humidity

# 编写工具类
@register_tool('get_humTemp')
class getHumTemp(BaseTool):
    description = "This tool can get the current humidity and temperature"
    parameters = [{}]
    requirement='该工具无需传递参数'

    def call(self, **kwargs) -> str:
        init_dht20()  # 初始化 DHT20
        res = ""
        for _ in range(3):
            temperature, humidity = read_dht20()  # 读取温湿度
            res = f"温度: {temperature:.2f}°C, 湿度: {humidity:.2f}%"
            time.sleep(1)  # 每秒读取一次
        return res