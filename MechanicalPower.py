import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, 
    QHBoxLayout, QWidget, QMessageBox, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

   

class MechanicalPower(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cálculo de Potência Mecânica")
        self.setGeometry(100, 100, 520, 360)

        self.setWindowIcon(QIcon('favicon/lungs.ico'))

        # Criando os widgets
        self.fr_label = QLabel("FR (rpm):")
        self.fr_input = QLineEdit()

        self.vt_label = QLabel("Vt (L):")
        self.vt_input = QLineEdit()

        self.pplat_label = QLabel("Pplat (cmH₂O):")
        self.pplat_input = QLineEdit()

        self.peep_label = QLabel("PEEP (cmH₂O):")
        self.peep_input = QLineEdit()

        self.raw_label = QLabel("Raw (cmH₂O/L/s):")
        self.raw_input = QLineEdit()

        self.flow_label = QLabel("Fluxo (L/min):")
        self.flow_input = QLineEdit()

        self.calc_mp_btn = QPushButton("Calcular Potência Mecânica")
        self.calc_mp_btn.clicked.connect(self.calcular_mp)

        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("font-size: 14px; font-weight: bold;")

        # Layout
        layout = QVBoxLayout()
        form_layouts = [
            (self.fr_label, self.fr_input),
            (self.vt_label, self.vt_input),
            (self.pplat_label, self.pplat_input),
            (self.peep_label, self.peep_input),
            (self.raw_label, self.raw_input),
            (self.flow_label, self.flow_input),
        ]

        max_label_width = max(label.sizeHint().width() for label, _ in form_layouts)

        max_label_width = max(label.sizeHint().width() for label, _ in form_layouts)

        for label, edit in form_layouts:
            h = QHBoxLayout()
            label.setFixedWidth(max_label_width + 30)  # Adiciona uma margem extra
            label.setAlignment(Qt.AlignVCenter | Qt.AlignRight)  # Centraliza na vertical e alinha à direita
            h.addWidget(label)
            h.addWidget(edit)
            layout.addLayout(h)


        layout.addWidget(self.calc_mp_btn)
        layout.addWidget(self.result_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Alinhamento central dos labels
        self.fr_label.setAlignment(Qt.AlignCenter)
        self.vt_label.setAlignment(Qt.AlignCenter)
        self.pplat_label.setAlignment(Qt.AlignCenter)
        self.peep_label.setAlignment(Qt.AlignCenter)
        self.raw_label.setAlignment(Qt.AlignCenter)
        self.flow_label.setAlignment(Qt.AlignCenter)


        # Aplica estilo
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: #f0f0f0;
                font-family: Arial;
                font-size: 13px;
            }
            QLineEdit {
                padding: 5px;
                border: 1px solid #555;
                border-radius: 6px;
                background: #3c3f41;
                color: #f0f0f0;
            }
            QPushButton {
                padding: 8px;
                border-radius: 8px;
                background-color: #0078d7;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
            QLabel {
                font-weight: bold;
            }
        """)

    def calcular_mp(self):
        try:
            fr = float(self.fr_input.text().replace(',', '.'))
            vt = float(self.vt_input.text().replace(',', '.'))
            pplat = float(self.pplat_input.text().replace(',', '.'))
            peep = float(self.peep_input.text().replace(',', '.'))
            raw = float(self.raw_input.text().replace(',', '.'))
            fluxo = float(self.flow_input.text().replace(',', '.'))
        except ValueError:
            QMessageBox.warning(self, "Erro", "Preencha todos os campos corretamente.")
            return

        try:
            ppico = (raw * fluxo / 60) + pplat
            delta = ppico - pplat - (peep * 0.5)
            mp = 0.098 * fr * vt * delta
        except Exception:
            QMessageBox.warning(self, "Erro", "Erro no cálculo. Verifique os dados de entrada.")
            return

        self.result_label.setText(
            # f"PPico calculado: {ppico:.2f} cmH₂O\nPotência Mecânica (MP): {mp:.2f} J/min"
            f"Potência Mecânica (MP): {mp:.2f} J/min"
        )

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MechanicalPower()
    window.show()
    sys.exit(app.exec_())
