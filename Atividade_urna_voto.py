from time import sleep

ana = 0
bruno = 0
carlos = 0
branco = 0


print("-=-" * 20)
print("\nUrna Gremio estudantil")
print(" ")
print("Escolha um candidato abaixo utilizando apenas numeros.")
print('''
[1] Ana
[2] Bruno
[3] Carlos
[0] Branco
''')
print("-=-" * 20)

for i in range (10):
    
    while True:
        voto = int(input(f"Eleitor {i+1}, digite seu voto: "))
        sleep (0.5)

        if voto == 1:
            ana += 1
            break
        elif voto == 2:
            bruno += 1
            break
        elif voto == 3:
            carlos += 1
            break
        elif voto == 0:
            branco += 1
            break
        else:
            print("VOTO INVALIDO! NAO SERÁ CONTABILIZADO, FAVOR DIGITAR UMA OPCAO VALIDA!")


if ana > bruno and ana > carlos:
    ana += branco
elif bruno > ana and bruno > carlos:
    bruno += branco
elif carlos > ana and carlos > bruno:
    carlos += branco

print("-=-" * 20)
print("\nRESULTADO FINAL")
print(f"Ana: {ana}")
print(f"Bruno: {bruno}")
print(f"Carlos: {carlos}")
print(f"Brancos: {branco}")


if ana > bruno and ana > carlos:
    print(f"\nVencedor: Ana com {ana} votos")
elif bruno > ana and bruno > carlos:
    print(f"\nVencedor: Bruno com {bruno} votos")
elif carlos > ana and carlos > bruno:
    print(f"\nVencedor: Carlos com {carlos} votos")
else:
    print("\nEmpate!")
print(" ")
print("-=-" * 20)


