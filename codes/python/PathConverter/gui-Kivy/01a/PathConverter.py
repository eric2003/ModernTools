import re
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.text import LabelBase

# 注册支持中文的字体
LabelBase.register(name='MicrosoftYaHei', fn_regular='C:/Windows/Fonts/msyh.ttc')

class PathConverterApp(App):
    def build(self):
        # 创建一个垂直布局
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # 创建输入路径的文本输入框
        self.input_path = TextInput(hint_text="请输入路径", multiline=False, font_name='MicrosoftYaHei')
        layout.add_widget(self.input_path)

        # 创建转换路径的按钮
        self.convert_button = Button(text="转换路径", font_name='MicrosoftYaHei')
        self.convert_button.bind(on_press=self.convert_path)
        layout.add_widget(self.convert_button)

        # 创建显示转换后路径的文本输入框（只读）
        self.output_path = TextInput(text="转换后的路径将显示在这里", readonly=True, multiline=False, font_name='MicrosoftYaHei')
        layout.add_widget(self.output_path)

        return layout

    def convert_path(self, instance):
        # 获取输入框中的路径并转换
        path = self.input_path.text
        converted_path = re.sub(r'\\', '/', path)
        # 显示转换后的路径
        self.output_path.text = converted_path

if __name__ == "__main__":
    PathConverterApp().run()