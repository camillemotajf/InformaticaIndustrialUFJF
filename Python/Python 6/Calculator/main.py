from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window

class MyWidget(GridLayout):
        
    def add_input(self, value):
        if self.ids.display.text == '0':
            self.ids.display.text = ''
        self.ids.display.text += str(value)
    
    def calculate_result(self):
        try:
            self.ids.display.text = str(eval(self.ids.display.text))
        except Exception:
            self.ids.display.text = "Error"

    def clear_display(self):
        self.ids.display.text = "0"
        
    def delete_last(self):
        self.display.text = self.display.text[:-1]

class Calculator(App):

    def build(self):
        return MyWidget()


if __name__ == '__main__':
    Window.size=(350,500)
    Calculator().run()