from rpi_TM1638 import TMBoards
TM = TMBoards(stb=17, clk=27, dio=22)
leds = [2,3]
for idx in leds:
  TM.leds[idx] = False

