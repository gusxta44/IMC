import sys
import PyQt5.QtWidgets
import PyQt5.uic
from calc_imc import calcular_imc, classificar_imc, peso_ideal
 
 
class IMC(PyQt5.QtWidgets.QDialog):
 
    def __init__(self):
        super().__init__()
        PyQt5.uic.loadUi("imc.ui", self)
        self.btnCalcular.clicked.connect(self.calcular)
        self.show()
 
    def calcular(self):
        try:
            peso = self.getPeso()
            altura = self.getAltura()
 
            imc = calcular_imc(peso, altura)
            classificacao = classificar_imc(imc)
 
            peso_min, peso_max = peso_ideal(altura)
 
            self.lblResultado.setText(
                f"IMC: {imc:.2f}\n"
                f"{classificacao}\n\n"
                f"Seu peso ideal deveria estar entre "
                f"{peso_min:.1f} kg e {peso_max:.1f} kg."
            )
 
        except ValueError:
            self.lblResultado.setText(
                "Caracteres inválidos. Use somente números."
            )
 
    def getPeso(self):
        peso = self.txtPeso.text()
        peso = peso.replace(",", ".")
        return float(peso)
 
    def getAltura(self):
        altura = self.txtAltura.text().strip()
 
        if not altura:
            raise ValueError
 
        altura = altura.replace(",", ".")
        altura = float(altura)
 
        if altura >= 100:
            altura = altura / 100
        return altura
 
if __name__ == "__main__":
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    janela = IMC()
    sys.exit(app.exec_())