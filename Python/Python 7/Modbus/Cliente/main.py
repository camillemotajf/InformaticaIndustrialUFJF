import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.clock import Clock

import threading
from pyModbusTCP.client import ModbusClient

class MyWidget(BoxLayout):
    pass

class ModbusApp(App):
    def build(self):
        self._ev = None
        return MyWidget()
    
    def create_connection(self, server_ip, porta, scan_time=1):
        self._cliente = ModbusClient(host=server_ip, port=porta)
        self._scan_time = scan_time       
        try:
            self._cliente.open()
            self.root.ids.status_label.text = "Status: Conectado"
        except Exception as e:
            self.root.ids.status_label.text = f"Status: Falha na conexão ({e})"

    def connect_to_server(self, *args):
        ip = self.root.ids.ip_input.text
        port = int(self.root.ids.port_input.text)
        self.root.ids.status_label.text = "Status: Conectando..."
        threading.Thread(target=self.create_connection, args=(ip, port)).start()

    def perform_read(self, button_id, addr):
        if button_id == 'bobina':
            return self._cliente.read_coils(addr, 1)[0]
        elif button_id == 'entrada_discreta':
            return self._cliente.read_discrete_inputs(addr, 1)[0]
        elif button_id == 'registrador_entrada':
            return self._cliente.read_input_registers(addr, 1)[0]
        elif button_id == 'registrador_saida':
            return self._cliente.read_holding_registers(addr, 1)[0]
        
    def update_reading(self, dt, button_id, addr):
        try:
            leitura = self.perform_read(button_id, addr)
            self.root.ids.leitura.text = f"Leitura: {leitura}"
        except Exception as e:
            self.root.ids.leitura.text = f"Erro: {e}"
        
    def choose_table(self, button_id):
        addr = int(self.root.ids.endereco.text)

        leitura_unica = self.root.ids.leitura_unica.active
        leitura_continua = self.root.ids.leitura_continua.active
        
        if leitura_unica:
            if self._ev:
                self._ev.cancel()
                self._ev = None
            self.update_reading(0, button_id, addr)
        
        elif leitura_continua:
            if self._ev:
                self._ev.cancel()
            self._ev = Clock.schedule_interval(lambda dt: self.update_reading(dt, button_id, addr), 1)

if __name__ == "__main__":
    Window.size = (800, 600)
    Window.fullscreen = False

    ModbusApp().run()
