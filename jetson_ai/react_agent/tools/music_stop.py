from react_agent.toolBase import BaseTool, register_tool
from react_agent.utils.AudioPlayer import player, songs

# 编写工具类
@register_tool('music_stop')
class MusicStop(BaseTool):
    description = 'This tool can be used to stop playing music.'
    parameters = [{}]
    requirement='该工具无需传递参数'

    def call(self, **kwargs) -> str:
        player.stop()
        return "成功关闭音乐"