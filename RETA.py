# DIMENSIONAMENTO DE PILARES SUBMETIDOS A FCN
# Desenvolvido por: Daniel D. Grossmann

from numpy import zeros, array, pi
from scipy import optimize


def deformacao(x, di):
    if 0 <= x <= (3.4999 / 13.5) * d11:
        return (10 / 1000) * (x - di) / (d11 - x)

    elif (3.5001 / 13.5) * d11 <= x <= 0.999 * altura:
        return (3.5 / 1000) * (x - di) / x

    else:
        return (14 / 1000) * (x - di) / (7 * x - 3 * altura)


def tensao(e):
    if e <= 2 / 1000:
        return e * 21000
    elif 2 / 1000 < e <= 10 / 1000:
        return 50 / 1.15
    else:
        print(f'\n\033[1;34m{"RESULTADO":=^70}\033[m')
        print('Erro! Deformação superior a 10/1000. Alterar informações inseridas.')
        print(f'\033[1;34m{"":=^70}\033[m')
        exit()


def fcc(x):
    if 0.8 * x < altura:
        return 0.8 * x * base * scd
    else:
        return 0.8 * altura * base * scd


def dcc(x):
    if 0.8 * x < altura:
        return 0.8 * x / 2 + (altura / 2 - 0.8 * x)
    else:
        return 0


def principal(x):
    for ii in range(n):
        tensoes[ii] = tensao(deformacao(x, posicoes[ii, 0]))

    soma_sigma = sum(tensoes)
    soma_sigma_y = sum(tensoes * posicoes[:, 1])
    # print(f'{soma_sigma} - {soma_sigma_y}')
    return (Md - fcc(x) * dcc(x)) * soma_sigma - (Nd - fcc(x)) * soma_sigma_y


def acha_x():
    if principal(0) * principal((3.4999 / 13.5) * d11) < 0:
        raiz = optimize.brentq(principal, 0, (3.4999 / 13.5) * d11)
        return raiz
    elif principal((3.5001 / 13.5) * d11) * principal(0.999 * altura) < 0:
        raiz = optimize.brentq(principal, (3.5001 / 13.5) * d11, 0.999 * altura)
        return raiz
    elif principal(1.001 * altura) * principal(10 ** 12) < 0:
        raiz = optimize.brentq(principal, 1.001 * altura, 10 ** 12)
        return raiz
    else:
        print(f'\n\033[1;34m{"RESULTADO":=^70}\033[m')
        print('Erro! Aumentar as dimensões do pilar e/ou número de barras.')
        print(f'\033[1;34m{"":=^70}\033[m')
        exit()


def area(x):
    for ii in range(n):
        tensoes1[ii] = tensao(deformacao(x, posicoes[ii, 0]))

    soma_sigma = sum(tensoes1)
    soma_sigma_y = sum(tensoes1 * posicoes[:, 1])

    if abs(round(soma_sigma, 4)) < 0.1:
        return (Md - dcc(x) * fcc(x)) / soma_sigma_y * n
    else:
        return (Nd - fcc(x)) / soma_sigma * n


# DADOS DE ENTRADA:
print(f'\n\033[1;32m{"DADOS GERAIS":=^70}\033[m')
print('1 - Propriedades geométricas:')
base = int(input('Base (cm): '))
altura = int(input('Altura (cm): '))

print('\n2 - Propriedades mecânicas e cobrimento:')
fck = float(input('Resistência característica do concreto a compressão (kN/cm²): '))
c = float(input('Cobrimento (cm): '))

print('\n3 - Esforços de cálculo:')
Nd = float(input('Esforço normal de cálculo (kN): '))
Md = float(input('Momento de cálculo (kNcm): '))

print(f'\033[1;32m{"":=^70}\033[m')

print(f'\n\033[1;36m{"DESCRIÇÃO DA ARMADURA":=^70}\033[m')

arranjo = input('Arranjo a utilizar [1,2,3...]: ')
arranjo = 'Arranjo ' + arranjo

while True:
    n = int(input('Número total de barras: '))

    if arranjo == 'Arranjo 1':
        n_linha_y = int(n / 2)
        break
    elif arranjo == 'Arranjo 2':
        n_linha_y = 2
        break
    else:
        if (n - 2 * arranjo[len(arranjo) - 1]) % 2 == 0:
            n_linha_y = int((n - 2 * arranjo[len(arranjo) - 1]) / 2)
            break
        else:
            print('Erro! Número total de barras equivocado.')
print(f'\033[1;36m{"":=^70}\033[m')

E = 21000

fi_t = 5
fi_l = 20

# CÁLCULOS
# Cálculo das alturas úteis
posicoes = zeros([n, 2])
tensoes = zeros(n)
tensoes1 = zeros(n)

d_linha = c + (fi_t + fi_l / 2) / 10

n_linha_x = []

if arranjo == 'Arranjo 1':

    for i in range(0, n_linha_y):
        n_linha_x.append(2)

elif arranjo == 'Arranjo 2':
    n_linha_x = [int(n / 2), int(n / 2)]
else:
    for i in range(0, n_linha_y):
        if i == 0 or i == n_linha_y - 1:
            n_linha_x.append(int(arranjo[len(arranjo) - 1]))
        else:
            n_linha_x.append(2)

k = i = 0
while k < n_linha_y:
    cont = 0
    while True:
        posicoes[i, 0] = d_linha + (n_linha_y - k - 1) * (altura - 2 * d_linha) / (n_linha_y - 1)
        posicoes[i, 1] = altura / 2 - posicoes[i, 0]

        cont += 1
        i += 1

        if cont == n_linha_x[k]:
            k += 1
            break

d11 = posicoes[0, 0]
scd = 0.85 * fck / 1.4

resp = acha_x()

As = area(resp)
print(f'\n\033[1;34m{"RESULTADO":=^70}\033[m')
print(f'Área de cálculo (As,calc) : {As:.2f} cm²')

area_barras = As / n
cont = 0
barras = [10, 12.5, 16, 20]

for i in range(len(barras)):
    if area_barras * 0.95 <= (barras[i] / 20) ** 2 * pi:
        bitola = barras[i]
        print(f'Arranjo a ser utilizado: {n}Ø{bitola} (As,ef = {(bitola/20)**2*pi*n:.2f} cm²)')
        cont = 1
        break

if cont == 0:
    print('Sem Arranjo disponível, escolher outra configuração de armadura.')
# 24.656482
print(f'\033[1;34m{"":=^70}\033[m')
