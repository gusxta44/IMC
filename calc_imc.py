def calcular_imc(peso, altura):
    imc = peso / (altura ** 2)
    return imc

def classificar_imc(imc):
    if imc < 18.5:
        return "Abaixo do peso"
    elif imc < 25:
        return "Peso normal"
    elif imc < 30:
        return "Sobrepeso"
    else:
        return "Obesidade"

def peso_ideal(altura):
    peso_min = 18.5 * (altura ** 2)
    peso_max = 24.9 * (altura ** 2)

    return peso_min, peso_max