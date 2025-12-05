from react_agent.toolBase import BaseTool, register_tool
import Jetson.GPIO as GPIO
import time

leds = [0 for _ ]

def callOn(leds, flag) -> str:
    from rpi_TM1638 import TMBoards

    TM = TMBoards(stb=17, clk=27, dio=22)
    for idx in range(8):
        print(TM.leds[idx])
    for idx in leds:
        TM.leds[idx-1] = flag
    # GPIO.cleanup()
    return "成功"

if __name__ == "__main__":
    callOn([1,3,4], True)
    time.sleep(5)
    callOn([1,3], False)
