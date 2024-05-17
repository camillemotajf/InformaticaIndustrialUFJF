from cliente import Cliente
import os


c = Cliente("127.0.0.1",9000)

caminho = r'C:\Users\camil\image_0002.jpg'
if not os.path.exists(caminho):
    print(f"File not found: {caminho}")
else:
    print(f"File exists: {caminho}")

    c.start(caminho=caminho)