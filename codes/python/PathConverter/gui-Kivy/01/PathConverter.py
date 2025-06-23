import re
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label

class PathConverterApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        self.input = TextInput(hint_text="请输入路径", multiline=False)
        self.layout.add_widget(self.input)
        self.button = Button(text="转换路径")
        self.button.bind(on_press=self.convert_path)
        self.layout.add_widget(self.button)
        self.output = TextInput(text="转换后的路径将显示在这里", readonly=True, multiline=False)
        self.layout.add_widget(self.output)
        return self.layout

    def convert_path(self, instance):
        path = self.input.text
        converted_path = re.sub(r'\\', '/', path)
        self.output.text = converted_path

if __name__ == "__main__":
    PathConverterApp().run()