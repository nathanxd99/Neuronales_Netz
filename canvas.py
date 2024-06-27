from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

class Canvas(QtWidgets.QLabel):
    """
    Eine Zeichenfläche, die es dem Benutzer ermöglicht, Ziffern zu zeichnen.
    
    Diese Klasse erweitert QLabel und bietet Funktionen zum Zeichnen, Speichern und Löschen von Bildern.
    """

    def __init__(self):
        """
        Initialisiert die Zeichenfläche.

        Erstellt ein Pixmap-Objekt mit einer schwarzen Hintergrundfarbe und setzt die Stiftfarbe auf Weiß.
        """
        super().__init__()
        pixmap = QtGui.QPixmap(280, 280)
        pixmap.fill(Qt.black)
        self.setPixmap(pixmap)

        self.last_x, self.last_y = None, None
        self.pen_color = QtGui.QColor(Qt.white)

    def set_pen_color(self, c):
        """
        Setzt die Stiftfarbe auf die angegebene Farbe.

        Args:
            c (QColor): Die neue Farbe für den Stift.
        """
        self.pen_color = QtGui.QColor(c)


    def mouseMoveEvent(self, e):
        """
        Behandelt das Ereignis, wenn die Maus über die Zeichenfläche bewegt wird.

        Zeichnet eine Linie vom letzten Punkt zur aktuellen Mausposition.

        Args:
            e (QMouseEvent): Das Mausereignis.
        """
        if self.last_x is None:
            self.last_x = e.x()
            self.last_y = e.y()
            return

        current_x = e.pos().x()
        current_y = e.pos().y()

        painter = QtGui.QPainter(self.pixmap())
        pen = QtGui.QPen(self.pen_color)
        pen.setWidth(10)
        painter.setPen(pen)
        painter.drawLine(self.last_x, self.last_y, current_x, current_y)
        painter.end()
        self.update()

        self.last_x = current_x
        self.last_y = current_y


    def mouseReleaseEvent(self, e):
        """
        Behandelt das Ereignis, wenn die Maus auf der Zeichenfläche losgelassen wird.

        Setzt die letzten Mauspositionen auf None.

        Args:
            e (QMouseEvent): Das Mausereignis.
        """
        self.last_x = None
        self.last_y = None
    
    def save_image(self, filename):
        """
        Speichert das aktuelle Bild der Zeichenfläche als Datei.

        Args:
            filename (str): Der Name der Datei, in der das Bild gespeichert werden soll.
        """
        self.pixmap().save(filename)

    def get_image_data(self):
        """
        Konvertiert das Bild der Zeichenfläche in eine Liste von Graustufenwerten.

        Das Bild wird auf 28x28 Pixel skaliert und in ein Graustufenformat konvertiert.

        Returns:
            list: Eine Liste von Graustufenwerten des Bildes.
        """
        image = self.pixmap().toImage()
        image = image.convertToFormat(QtGui.QImage.Format_Grayscale8)
        image = image.scaled(28, 28, QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
        
        data = []
        for y in range(28):
            for x in range(28):
                pixel_value = image.pixelColor(x, y).black()  # Schwarz gibt den Graustufenwert zurück
                data.append(pixel_value)
        
        return data

    def clear(self):
        """
        Löscht die Zeichenfläche, indem sie mit schwarzer Farbe gefüllt wird.
        """
        pixmap = self.pixmap()
        pixmap.fill(Qt.black)
        self.setPixmap(pixmap)
        self.update()
