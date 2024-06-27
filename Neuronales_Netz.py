# Selbst programmiertes neuronales Netz
#
# Autor: Luca Glaser

# Imports
from matrix import Matrix
from mnist import MNIST
from time import perf_counter as pfc, sleep
import sys
from PyQt5 import QtWidgets
from mainWindow import MainWindow
import winsound


def doASound():
    # Frequenz in Hertz
    frequency = 300
    # Dauer in Millisekunden
    duration = 400
    # Anzahl der Wiederholungen
    repeats = 3
    for _ in range(repeats):
        winsound.Beep(frequency, duration)
        sleep(0.001)

def write_gewMat(filename, gewMat):
    """
    Schreibt eine übergebene Matrix in eine Textdatei

    Args:
        filename (String): Der Name der Datei, in die, die Matrix geschrieben wird
        gewMat (Matrix): Die Matrix, die in die Datei geschrieben werden soll

    Returns:
        None
    """
    s = ""
    with open(filename,"w") as f:
        for row in range(gewMat.rows):
            for column in range(gewMat.columns):
                s += str(gewMat.data[row][column])
                if column < gewMat.columns -1:
                    s += " "
            if row < gewMat.rows -1:
                s += "\n"
        f.write(s)

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

def gewichte_initialisieren():

    gewichtungsMat1 = Matrix(100, 784, "Xavier")
    write_gewMat(file_GewMat1,gewichtungsMat1)
    gewichtungsMat2 = Matrix(10, len(gewichtungsMat1.data[0]), "Xavier")
    write_gewMat(file_GewMat2,gewichtungsMat2)
    print("Done")

def neuronales_Netz(TRAIN, TEST, EIGENEZIFFERN, gewichtungsMat1, gewichtungsMat2):
    
    if TRAIN or TEST:
        mndata = MNIST('images')

        # Einlesen der Trainings- und Test-Daten
        train_images, train_labels = mndata.load_training()
        test_images, test_labels = mndata.load_testing()
    
    if TRAIN:
        lernrate = 0.05

        for index in range(len(train_images)):

            label = train_labels[index]
            image = train_images[index]
            
            gewichtungsMat2T = gewichtungsMat2.transponieren()
            
            inputMatT = Matrix(1,len(image), image)
            inputMat = inputMatT.transponieren()
            inputMat / 255

            zwischenschichtMat = gewichtungsMat1 * inputMat
            zwischenschichtMat = zwischenschichtMat.sigmoid()

            outputMat = gewichtungsMat2 * zwischenschichtMat
            outputMat = outputMat.sigmoid()

            outputExpected = Matrix(10,1)
            outputExpected.data[label][0] = 1

            outputError = Matrix(10, 1)
            for i in range(outputError.columns):
                outputError.data[i][0] = outputExpected.data[i][0]-outputMat.data[i][0]

            hiddenError = gewichtungsMat2T * outputError

            dsigZwischenschichtMat = zwischenschichtMat.dsigmoid()

            zwischenschichtMatBias = Matrix(zwischenschichtMat.rows, zwischenschichtMat.columns)

            for row in range(zwischenschichtMat.rows):
                for column in range(zwischenschichtMat.columns):
                    zwischenschichtMatBias.data[row][column] = hiddenError.data[row][column]*dsigZwischenschichtMat.data[row][column]

            zwischenschichtMatBias *= lernrate
            gewichtungsMat1Error = zwischenschichtMatBias * inputMatT

            for row in range(gewichtungsMat1.rows):
                for column in range(gewichtungsMat1.columns):
                    gewichtungsMat1.data[row][column] = gewichtungsMat1.data[row][column] + gewichtungsMat1Error.data[row][column]

            zwischenschichtMatT = zwischenschichtMat.transponieren()

            dsigOutputMat = outputMat.dsigmoid()

            outputMatBias = Matrix(outputMat.rows, outputMat.columns)

            for row in range(outputMat.rows):
                for column in range(outputMat.columns):
                    outputMatBias.data[row][column] = outputError.data[row][column]*dsigOutputMat.data[row][column]

            outputMatBias *=  lernrate
            gewichtungsMat2Error = outputMatBias * zwischenschichtMatT

            for row in range(gewichtungsMat2.rows):
                for column in range(gewichtungsMat2.columns):
                    gewichtungsMat2.data[row][column] = gewichtungsMat2.data[row][column] + gewichtungsMat2Error.data[row][column]

        write_gewMat(file_GewMat1,gewichtungsMat1)
        write_gewMat(file_GewMat2,gewichtungsMat2)

    if TEST:
    
        richtigeZiffern = 0

        for index in range(len(test_images)):

            label = test_labels[index]
            image = test_images[index]

            inputMatT = Matrix(1,len(image), image)
            inputMat = inputMatT.transponieren()
            inputMat / 255

            zwischenschichtMat = gewichtungsMat1 * inputMat
            zwischenschichtMat = zwischenschichtMat.sigmoid()

            outputMat = gewichtungsMat2 * zwischenschichtMat
            outputMat = outputMat.sigmoid()

            outputMat = outputMat.transponieren()

            if outputMat.data[0][label] == max(outputMat.data[0]):
                richtigeZiffern += 1
            
            # print(outputMat.data)
        print(richtigeZiffern/len(test_images) * 100)
    

    if EIGENEZIFFERN:
        app = QtWidgets.QApplication(sys.argv)
        window = MainWindow()
        window.show()
        app.exec_()


if __name__ == "__main__":
    start = pfc()

    TRAIN = False
    TEST = False
    EIGENEZIFFERN = True
    GEWICHTENEUINITIALISIEREN = False

    file_GewMat1 = "gewichtungsmatrix1.txt"
    file_GewMat2 = "gewichtungsmatrix2.txt"

    if GEWICHTENEUINITIALISIEREN:
        gewichte_initialisieren()
    
    gewichtungsMat1 = Matrix(100, 784, get_gewMat(file_GewMat1))
    gewichtungsMat2 = Matrix(10, len(gewichtungsMat1.data), get_gewMat(file_GewMat2))

    neuronales_Netz(TRAIN, TEST, EIGENEZIFFERN, gewichtungsMat1, gewichtungsMat2)

    print(pfc()-start)

    # doASound()