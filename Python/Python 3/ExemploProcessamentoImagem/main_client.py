from cliente import Cliente
import os


c = Cliente("127.0.0.1",9000)

caminho = r'C:\Users\camil\OneDrive\Área de Trabalho\Inf_Ind\InformaticaIndustrialUFJF\Python\Python 3\ExemploProcessamentoImagem\faces\image_0001.jpg'
if not os.path.exists(caminho):
    print(f"File not found: {caminho}")
else:
    print(f"File exists: {caminho}")

    c.start(caminho=caminho)