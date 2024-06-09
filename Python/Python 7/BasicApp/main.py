import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

class MyWidget(BoxLayout):
    def incrementar(self):
        c = int(self.ids.lb.text)
        if self.ids.input.text:
            c += int(self.ids.input.text)
        else:
            c += 1
        self.ids.lb.text = str(c)


class BasicApp(App):
    def build(self):
        """
        Método para construção do aplicativo com base no widget criado
        """
        return MyWidget()
 
if __name__ == '__main__':
    Window.size=(800,600)
    Window.fullscreen = False
    BasicApp().run()