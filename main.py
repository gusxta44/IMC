import os
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
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
            sexo = self.getSexo()

            imc = calcular_imc(peso, altura)
            categoria = classificar_imc(imc)
            classificacao = self.formatar_classificacao(categoria)
            peso_min, peso_max = peso_ideal(altura)

            self.lblResultado.setText(
                f"IMC: {imc:.2f}\n"
                f"{classificacao}\n\n"
                f"Seu peso ideal deve estar entre "
                f"{peso_min:.1f} kg e {peso_max:.1f} kg."
            )

            caminho_img = self.get_classification_image(classificacao, sexo)
            if caminho_img:
                pixmap = QPixmap(caminho_img)
                if not pixmap.isNull():
                    pixmap = pixmap.scaledToWidth(220, Qt.SmoothTransformation)
                    self.lblImagem.setPixmap(pixmap)
                else:
                    self.lblImagem.clear()
            else:
                self.lblImagem.clear()

        except ValueError:
            self.lblResultado.setText("Caracteres inválidos. Use somente números.")
            self.lblImagem.clear()

    def formatar_classificacao(self, categoria):
        categoria = categoria.strip()
        if categoria in ("Abaixo do peso", "Peso normal", "Sobrepeso", "Obesidade"):
                return f"{categoria}"

        return categoria

    def getPeso(self):
        peso = self.txtPeso.text().replace(",", ".")
        return float(peso)

    def getSexo(self):
        sexo = self.comboBox.currentText().strip()
        if sexo == "Masculino":
            return "M"
        if sexo == "Feminino":
            return "F"
        raise ValueError("Sexo não selecionado")

    def getAltura(self):
        altura = self.txtAltura.text().strip()
        if not altura:
            raise ValueError

        altura = float(altura.replace(",", "."))
        if altura >= 100:
            altura = altura / 100
        return altura

    def get_classification_image(self, classificacao, sexo):
        imagens = {
            "Abaixo do peso": {
                "M": "images/abaixo.png",
                "F": "images/feminino_abaixo.png"
            },
            "Peso normal": {
                "M": "images/normal.png",
                "F": "images/feminino_normal.png"
            },
            "Sobrepeso": {
                "M": "images/sobrepeso.png",
                "F": "images/feminino_sobrepeso.png"
            },
            "Obesidade": {
                "M": "images/obeso.png",
                "F": "images/feminino_obeso.png"
            }
        }

        categoria = imagens.get(classificacao)
        if not categoria:
            return None

        escolha = categoria.get(sexo, categoria.get("M"))
        base_dir = os.path.dirname(os.path.abspath(__file__))
        caminho = os.path.normpath(os.path.join(base_dir, escolha))
        return caminho if os.path.isfile(caminho) else None

if __name__ == "__main__":
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    janela = IMC()
    sys.exit(app.exec_())