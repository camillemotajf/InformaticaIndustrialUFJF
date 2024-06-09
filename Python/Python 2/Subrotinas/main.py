def soma(op1, op2):
    return op1 + op2

def divisao(dividendo, divisor ):
    return dividendo/divisor

def incremento(num):
    num +=1 # modificação feita dentro da subrotina
    print("Numero com o incremento: ", num)

def incrementoLista(lista):
    lista.append(1) # modificação feita dentro da subrotina
    return lista

a = 3
b = 2
lista_main = [5, 8, 7, 6]

print("Antes do Incremento: ", a)
incremento(a)
print("Depois do Incremento: ",a)

lista_main_new = incrementoLista(lista_main)
print(id(lista_main))
print(id(lista_main_new))
print(lista_main)
print(lista_main_new)