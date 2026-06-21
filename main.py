import os
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.core.audio import SoundLoader
from kivy.clock import Clock

# KV-разметка интерфейса
KV = '''
MDBoxLayout:
    orientation: 'vertical'
    padding: "10dp"
    spacing: "10dp"

    # Видео-зона (черный экран, если режим "Только звук")
    MDBoxLayout:
        id: video_container
        md_bg_color: 0, 0, 0, 1
        size_hint_y: 0.5
        MDLabel:
            id: video_status
            text: "Плеер готов"
            halign: "center"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1

    # Ползунок перемотки трека/видео
    MDSlider:
        id: progress_slider
        min: 0
        max: 100
        value: 0
        on_touch_up: app.set_position(self.value)

    # Панель управления (Назад, Плей/Пауза, Вперед)
    MDBoxLayout:
        orientation: 'horizontal'
        spacing: "20dp"
        adaptive_size: True
        pos_hint: {"center_x": .5}

        MDIconButton:
            icon: "rewind-10"
            on_press: app.seek_relative(-10)

        MDIconButton:
            id: play_btn
            icon: "play"
            on_press: app.toggle_play()

        MDIconButton:
            icon: "fast-forward-10"
            on_press: app.seek_relative(10)

    # Настройка экстремальной громкости (усиление)
    MDBoxLayout:
        orientation: 'horizontal'
        spacing: "10dp"
        size_hint_y: None
        height: "40dp"

        MDIcon:
            icon: "volume-high"
            pos_hint: {"center_y": .5}

        MDSlider:
            id: volume_slider
            min: 0
            max: 200  # До 200% для "прям громко"
            value: 100
            on_value: app.change_volume(self.value)

        MDLabel:
            text: f"{int(volume_slider.value)}%"
            adaptive_width: True
            pos_hint: {"center_y": .5}

    # Переключатель "Только звук в фоне"
    MDBoxLayout:
        orientation: 'horizontal'
        size_hint_y: None
        height: "50dp"
        
        MDLabel:
            text: "Режим: Только звук (фон)"
            pos_hint: {"center_y": .5}
            
        MDSwitch:
            id: audio_only_switch
            pos_hint: {"center_y": .5}
            on_active: app.toggle_audio_only(self.active)
'''

class MediaPlayerApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        
        # Ссылка на файл (замените на свой mp3/mp4)
        self.media_file = "sample.mp4" 
        self.sound = None
        self.is_playing = False
        
        # Обновление слайдера каждую секунду
        Clock.schedule_interval(self.update_progress, 1)
        
        return Builder.load_string(KV)

    def load_media(self):
        if not self.sound and os.path.exists(self.media_file):
            self.sound = SoundLoader.load(self.media_file)

    def toggle_play(self):
        self.load_media()
        if not self.sound:
            self.root.ids.video_status.text = "Файл не найден!"
            return

        if self.is_playing:
            self.sound.stop()
            self.root.ids.play_btn.icon = "play"
            self.is_playing = False
        else:
            self.sound.play()
            self.root.ids.play_btn.icon = "pause"
            self.is_playing = True
            # Применяем текущую громкость при старте
            self.change_volume(self.root.ids.volume_slider.value)

    def change_volume(self, value):
        if self.sound:
            # В Kivy базовый диапазон 0.0 - 1.0. 
            # Деление на 100 позволяет делать звук тише/громче, 
            # а значение слайдера до 200 дает программное усиление.
            self.sound.volume = value / 100.0

    def seek_relative(self, seconds):
        if self.sound:
            current = self.sound.get_pos()
            new_pos = max(0, current + seconds)
            self.sound.seek(new_pos)

    def set_position(self, percentage):
        if self.sound:
            duration = self.sound.length
            if duration > 0:
                target_pos = (percentage / 100.0) * duration
                self.sound.seek(target_pos)

    def update_progress(self, dt):
        if self.sound and self.is_playing:
            pos = self.sound.get_pos()
            dur = self.sound.length
            if dur > 0:
                self.root.ids.progress_slider.value = (pos / dur) * 100

    def toggle_audio_only(self, active):
        if active:
            self.root.ids.video_status.text = "Режим аудио: видео отключено"
            # Здесь логика отключения видео-текстуры для экономии батареи в фоне
        else:
            self.root.ids.video_status.text = "Режим видео"
            
if __name__ == '__main__':
    MediaPlayerApp().run()
