import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QMessageBox
)
from PyQt5.QtCore import Qt

class PotenciaGattinoniApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cálculo de Potência Mecânica (Gattinoni)")
        self.setGeometry(100, 100, 500, 330)

        # Criando os widgets
        self.fr_label = QLabel("FR (rpm):")
        self.fr_input = QLineEdit()

        self.vt_label = QLabel("Vt (L):")
        self.vt_input = QLineEdit()

        self.pplat_label = QLabel("Pplat (cmH₂O):")
        self.pplat_input = QLineEdit()

        self.peep_label = QLabel("PEEP (cmH₂O):")
        self.peep_input = QLineEdit()

        self.ppico_label = QLabel("PPico (cmH₂O):")
        self.ppico_input = QLineEdit()
        self.ppico_input.setPlaceholderText("Opcional")

        self.raw_label = QLabel("Raw (cmH₂O/L/s):")
        self.raw_input = QLineEdit()

        self.flow_label = QLabel("Fluxo (L/min):")
        self.flow_input = QLineEdit()

        self.calc_ppico_btn = QPushButton("Calcular PPico")
        self.calc_ppico_btn.clicked.connect(self.calcular_ppico)

        self.calc_mp_btn = QPushButton("Calcular Potência Mecânica")
        self.calc_mp_btn.clicked.connect(self.calcular_mp)

        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignCenter)

        # Layouts
        layout = QVBoxLayout()
        form_layouts = [
            (self.fr_label, self.fr_input),
            (self.vt_label, self.vt_input),
            (self.pplat_label, self.pplat_input),
            (self.peep_label, self.peep_input),
            (self.ppico_label, self.ppico_input),
            (self.raw_label, self.raw_input),
            (self.flow_label, self.flow_input),
        ]
        for label, edit in form_layouts:
            h = QHBoxLayout()
            h.addWidget(label)
            h.addWidget(edit)
            layout.addLayout(h)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.calc_ppico_btn)
        btn_layout.addWidget(self.calc_mp_btn)
        layout.addLayout(btn_layout)
        layout.addWidget(self.result_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def calcular_ppico(self):
        try:
            raw = float(self.raw_input.text().replace(',', '.'))
            fluxo = float(self.flow_input.text().replace(',', '.'))
            pplat = float(self.pplat_input.text().replace(',', '.'))
        except ValueError:
            QMessageBox.warning(self, "Erro", "Preencha Raw, Fluxo e Pplat corretamente.")
            return

        ppico = (raw * fluxo / 60) + pplat
        self.ppico_input.setText(f"{ppico:.2f}")
        self.result_label.setText(f"PPico calculado: {ppico:.2f} cmH₂O")

    def calcular_mp(self):
        # Checando e lendo entradas
        try:
            fr = float(self.fr_input.text().replace(',', '.'))
            vt = float(self.vt_input.text().replace(',', '.'))
            pplat = float(self.pplat_input.text().replace(',', '.'))
            peep = float(self.peep_input.text().replace(',', '.'))
        except ValueError:
            QMessageBox.warning(self, "Erro", "Preencha FR, Vt, Pplat e PEEP corretamente.")
            return

        # PPico: pode estar vazio -> tenta calcular se há raw/fluxo
        ppico_text = self.ppico_input.text().replace(',', '.')
        ppico = None
        if ppico_text == '':
            try:
                raw = float(self.raw_input.text().replace(',', '.'))
                fluxo = float(self.flow_input.text().replace(',', '.'))
                ppico = (raw * fluxo / 60) + pplat
            except ValueError:
                QMessageBox.warning(self, "Erro", "Informe PPico ou Raw, Fluxo e Pplat para calcular automaticamente.")
                return
        else:
            try:
                ppico = float(ppico_text)
            except ValueError:
                QMessageBox.warning(self, "Erro", "Valor de PPico inválido.")
                return

        # Cálculo principal
        try:
            delta = ppico - pplat - (peep * 0.5)
            mp = 0.098 * fr * vt * delta
        except Exception:
            QMessageBox.warning(self, "Erro", "Erro no cálculo. Verifique os dados de entrada.")
            return

        self.result_label.setText(
            f"PPico usado: {ppico:.2f} cmH₂O\nPotência Mecânica (MP): {mp:.2f} J/min"
        )

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PotenciaGattinoniApp()
    window.show()
    sys.exit(app.exec_())
