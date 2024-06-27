from matrix import Matrix
from canvas import Canvas
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np

class MainWindow(QtWidgets.QMainWindow):
    """
    Hauptfenster für die MNIST-Ziffernerkennung.
    
    Diese Klasse erstellt ein Hauptfenster mit einer Zeichenfläche, auf der der Benutzer Ziffern zeichnen kann.
    Das Fenster enthält Schaltflächen zum Speichern und Vorhersagen der gezeichneten Ziffer sowie zum Löschen der Zeichnung.
    """

    def __init__(self):
        """
        Initialisiert das Hauptfenster.

        Setzt den Fenstertitel, die Geometrie und erstellt die Zeichenfläche und die Schaltflächen.
        """
        super().__init__()
        self.file_GewMat1 = "gewichtungsmatrix1.txt"
        self.file_GewMat2 = "gewichtungsmatrix2.txt"

        self.setWindowTitle('MNIST Digit Drawer')
        self.setGeometry(100, 100, 400, 400)

        self.canvas = Canvas()
        self.setCentralWidget(self.canvas)

        save_button = QtWidgets.QPushButton('Save and Predict', self)
        save_button.clicked.connect(self.save_and_predict)
        
        clear_button = QtWidgets.QPushButton('Clear', self)
        clear_button.clicked.connect(self.canvas.clear)

        self.addToolBar(QtCore.Qt.BottomToolBarArea, self.create_tool_bar(save_button, clear_button))

    def create_tool_bar(self, *buttons):
        """
        Erstellt eine Werkzeugleiste mit den angegebenen Schaltflächen.

        Args:
            *buttons: Variable Anzahl von Schaltflächen, die zur Werkzeugleiste hinzugefügt werden sollen.

        Returns:
            QtWidgets.QToolBar: Die erstellte Werkzeugleiste.
        """
        toolbar = QtWidgets.QToolBar()
        for button in buttons:
            toolbar.addWidget(button)
        return toolbar

    def save_and_predict(self):
        """
        Speichert die gezeichnete Ziffer als Bild und führt eine Vorhersage mit dem neuronalen Netz durch.
        """
        filename = 'digit.png'
        self.canvas.save_image(filename)
        data = self.canvas.get_image_data()
        prediction = self.neural_network_predict(data)
        print("Prediction:", prediction)

    def neural_network_predict(self, image_data):
        """
        Führt eine Vorhersage auf Basis der gezeichneten Ziffer durch.

        Args:
            image_data (list): Die Bilddaten der gezeichneten Ziffer.

        Returns:
            int: Die vorhergesagte Ziffer.
        """
        inputMatT = Matrix(1, len(image_data), image_data)
        inputMatT / 255
        inputMat = inputMatT.transponieren()

        gewichtungsMat1 = Matrix(100, len(image_data), get_gewMat(self.file_GewMat1))
        gewichtungsMat2 = Matrix(10, 100, get_gewMat(self.file_GewMat2))

        zwischenschichtMat = gewichtungsMat1 * inputMat
        zwischenschichtMat = zwischenschichtMat.sigmoid()

        outputMat = gewichtungsMat2 * zwischenschichtMat
        outputMat = outputMat.sigmoid()

        outputMat = outputMat * 100
        
        print(outputMat)

        return np.argmax([outputMat.data[i][0] for i in range(outputMat.rows)])
    
def get_gewMat(filename):
    """
    Liest eine Textdatei aus und gibt ein 2D-Array mit den Werten aus der Textdatei zurück

    Args:
        filename (String): Der Name der Datei, aus der die Matrix ausgelesen wird

    Returns:
        matData [list[list[float]]]: Das 2D-Array mit den Werten aus der Datei
    """
    matData = [[]]
    with open(filename) as f:
        for index,line in enumerate(f.read().splitlines()):
            for number in line.split():
                matData[index].append(float(number))
            matData.append([])
    return matData