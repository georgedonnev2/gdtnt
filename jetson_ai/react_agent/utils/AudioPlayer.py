import os
import random
import threading
import pygame

class AudioPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.current_thread = None
        self.is_playing = False
        self.current_song = None

    def play_random(self, songs):
        self.stop()  # 停止当前播放
        self.current_song = random.choice(songs)
        self.is_playing = True
        self.current_thread = threading.Thread(target=self._play_audio, args=(self.current_song,))
        self.current_thread.start()

    def _play_audio(self, song):
        pygame.mixer.music.load(song)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    def stop(self):
        if self.is_playing:
            print("Stopping audio...")
            pygame.mixer.music.stop()
            self.is_playing = False

    def switch_song(self, songs):
        if self.is_playing:
            print("Switching song...")
            self.stop()
        self.play_random(songs)

# 音乐目录和文件列表 (实例化)
music_dir = "music"
songs = [os.path.join(music_dir, file) for file in os.listdir(music_dir) if file.endswith(".mp3")]
player = AudioPlayer()