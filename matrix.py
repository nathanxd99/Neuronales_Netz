# !bin/env python3
"""
Hier ist die Klasse Matrix definiert.
Programmname: matrix.py
Autor: Luca Glaser
Erstellt am: 2023/03/01
"""

import math
import random


class Matrix:
    """
    Die Klasse Matrix dient dazu um Matrizen als Objekte zu erstellen.

    Attributes:
        rows (int) = Anzahl der Reihen.
        columns (int) = Anzahl der Spalten.
        data (List[List[float]]) = Die Werte, die in der Matrix stehen.

    """

    def __init__(self,rows,columns, data=None):
        """
        Dient der Initialisierung eines Matrix-Objekts.

        Args:
            rows (int) = Anzahl der Reihen.
            columns (int) = Anzahl der Spalten.
            data (List[List[float]]) = Die Werte, die in der Matrix stehen, mit dem Wert "0" initialisiert.
        """
        self.rows = rows
        self.columns = columns
        self.data = [[0 for _ in range(columns)] for _ in range(rows)]
        # Es wurde ein Integer oder Float übergeben, mit diesem wird die Matrix gefüllt
        if type(data) == int or type(data) == float:
            self.data = [[data for _ in range(columns)] for _ in range(rows)]
        # Es wurde ein Vektor oder eine Matrix übergeben und die wird übernommen
        elif type(data) == list:
            # Es wurde eine Matrix übergeben
            if type(data[0]) == list:
                for row in range(self.rows):
                    for column in range(self.columns):
                        self.data[row][column] = data[row][column]
            # Es wurde ein Vektor übergeben
            else:
                for column in range(self.columns):
                    self.data[0][column] = data[column]
        elif type(data) == str and data == "Random":
            for row in range(self.rows):
                for column in range(self.columns):
                    self.data[row][column] = random.random()
        elif type(data) == str and data == "Xavier":
            for row in range(self.rows):
                for column in range(self.columns):
                    self.data[row][column] = random.uniform(-(1/self.rows), (1/self.rows))
        
            
    def __str__(self):
        """
        Dient dazu um das Matrix-Objekt als String auszugeben.

        Returns:
            Ein String, der die Werte in der Matrix, ordentlich aufgelistet, zurück gibt.
        """
        s = ""
        for i in range(self.rows):
            for j in range(self.columns):
                s += f"{self.data[i][j]:>4}"
            s += "\n"
        return s
    
    def __add__(self, other):
        """
        Dient dazu um zwei Matrix-Objekte miteinander zu addieren.

        Args:
            other (Matrix) = Ein Matrix-Objekt mit dem addiert wird.

        :raises SizeError: Wenn die Matritzen unterschiedliche Anzahl an Reihen oder Spalten hat.
                           Die "self"-Matrix wird dabei zurück gegeben.

        Returns:
            Gibt eine Liste aus Listen mit den Werten der neuen Matrix zurück.
        """
        if self.rows!=other.rows or self.columns!=other.columns:
            print("Matrices have to be the same size")
            return self.data
        new_m = Matrix(self.rows, self.columns)
        for i in range(self.rows):
            for j in range(self.columns):
                new_m.data[i][j] = self.data[i][j] + other.data[i][j]
        return new_m.data

    def __mul__(self, other):
        """
        Dient dazu um zwei Matrix-Objekte miteinander zu multiplizieren oder eine Matrix mit einem Skalar zu multiplizieren.

        Args:
            other (Matrix) = Ein Matrix-Objekt mit dem multipliziert wird.

        Returns:
            Gibt eine Liste aus Listen mit den Werten der neuen Matrix zurück.
        """
        if isinstance(other,Matrix):
            if self.columns!=other.rows:
                print("The amount of columns of the first and the amount of rows of the second Matrix have to be the same!")
                return self.data
            new_m = Matrix(self.rows, other.columns)
            for m in range(self.rows):
                for r in range(other.columns):
                    for n in range(self.columns):
                        new_m.data[m][r] += self.data[m][n] * other.data[n][r]
            return new_m

        new_m = Matrix(self.rows,self.columns)
        for row in range(self.rows):
            for column in range(self.columns):
                new_m.set_value(row,column,self.data[row][column]*other)
        return new_m
    
    
    def __truediv__(self,other):
        """
        Dient dazu um eine Matrix durch ein Skalar zu teilen.

        Args:
            other (Skalar) = Ein Integer durch den die Matrix geteilt wird.
        
        Returns:
            Gibt eine neue Matrix mit den angepassten Werten an.
        """
        for row in range(self.rows):
            for column in range (self.columns):
                self.set_value(row,column,self.data[row][column]/other)

    
    def get_value(self,row,column):
        """
        Gibt den Wert von einem Punkt in der Matrize zurück

        Args:
            row = Reihe von dem erwarteten Wert
            column = Spalte von dem erwarteten Wert

        Returns:
            Gibt den entsprechenden Wert aus der Matrix zurück
        """
        return self.data[row][column]

    
    def set_value(self,row,column,value):
        """
        Ändert den entsprechenden Wert aus der Matrix

        Args:
            row = Zeile von dem zu ändernden Wert
            column = Spalte von dem zu ändernden Wert
            value = Neuer Wert der an der entsprechenden Stelle eingesetzt wird
        """
        self.data[row][column] = value

    
    def transponieren(self):
        """
        Transponiert die eigene Matrix und gibt sie transponiert zurück

        Returns:
            Gibt die eigene Matrix transponiert zurück
        """
        new_m = Matrix(self.columns, self.rows)
        for row in range(self.rows):
            for column in range(self.columns):
                new_m.data[column][row] = self.data[row][column]
        # self.rows,self.columns,self.data = new_m.rows,new_m.columns,new_m.data
        return new_m
            

    def determinant(self):
        """
        Dient dazu um die Determinante der Matrix zu berechnen.

        Args:
            det (int) = Wert der Determinante.
            minor (Matrix) = Verkleinerte Matrix.

        :raises SizeError: Wenn die Matrix keine Quadratische Matrix ist.
                           None wird zurück gegeben. 

        Returns:
            Es wird die Determinante zurück gegeben.
        """
        
        if self.rows != self.columns:
            print("Determinant is only defined for squared matrices")
            return None
        if self.rows == 2:
            return self.data[0][0] * self.data[1][1] - self.data[0][1] * self.data[1][0]
        if self.rows == 3:
            return self.data[0][0] * self.data[1][1] * self.data[2][2] + self.data[0][1] * self.data[1][2] * self.data[2][0] + self.data[0][2] * self.data[1][0] * self.data[2][1] - self.data[2][0] * self.data[1][1] * self.data[0][2] - self.data[2][1] * self.data[1][2] * self.data[0][0] - self.data[2][2] * self.data[1][0] * self.data[0][1] 
        det = 0
        for i in range(self.columns):
            minor = self.create_minor(0,i)
            det += ((-1)**i) * self.data[0][i] * minor.determinant()
        return det

    def create_minor(self, row, column):
        """
        Dient dazu eine kleinere Matrix zu erstellen.

        Args:
            row (int) = Nummer der zu entfernenden Reihe aus der zu verkleinernden Matrix.
            column (int) = Nummer der zu entfernenden Spalte aus der zu verkleinernden Matrix.
            minor (Matrix) = Matrix-Objekt der verkleindenden Matrix.
            minor_row (int) = Nummer der Reihe in die der Wert, bei der verkleinerten Matrix, eingetragen wird.
            minor_column (int) = Nummer der Spalte in die der Wert, bei der verkleinerten Matrix, eingetragen wird.

        Returns:
            Gibt die verkleinernde Matrix als Matrix-Objekt zurück.
        """
        minor = Matrix(self.rows-1, self.columns-1)
        for i in range(self.rows):
            for j in range(self.columns):
                if i != row and j != column:
                    minor_row = i if i < row else i-1
                    minor_column = j if j < column else j-1
                    minor.set_value(minor_row, minor_column, self.data[i][j])
        return minor

    def get_x_values(self,v):
        """
        Dient dazu ein LGS mithilfe einer Matrix und einem Vektor zu lösen.

        Args:
            v (List(int)) = Ein Vektor als Liste mit den Koordinaten des Vektors als Elemente der Liste.
            new_m (Matrix) = Neue Matrix wenn man den Vektor v gegen eine der Spalten der Matrix ersetzt.
            x (List(float)) = Die Werte die für herauskommen, wenn man das LGS aus der Matrix new_m löst.

        :raises ValueError: Wenn die Länge der Liste v nicht mit der Länge der Reihen oder Spalten der Matrix übereinstimmt.

        Returns:
            Gibt die Liste x mit den Werten zurück, die herauskommen, wenn man das LGS löst.
        """
        if len(v) != self.rows:
            print("You can only get x-Values if the length of v and the length of the rows is equal!!")
            return [0]
        new_m = Matrix(self.rows,self.columns)
        x = []
        for y in range(self.columns):
            for i in range(self.rows):
                for j in range(self.columns):
                    new_m.data[i][j] = v[i] if y == j else self.data[i][j]
            x.append(new_m.determinant()/self.determinant())
        return x
    

    def sigmoid(self):
        """
        Aktiviert die ganze Matrix mit der Sigmoid Funktion.
        Args:
            new_m (Matrix): Neu erstellte Matrix mit den aktivierten Werten

        Returns:
            new_m (Matrix): Die Sigmoid aktivierte Matrix
        """
        new_m = Matrix(self.rows, self.columns)
        for row in range(self.rows):
            for column in range(self.columns):
                new_m.data[row][column] = 1/(1+math.exp(-self.data[row][column]))
                    
        return new_m

    def dsigmoid(self):
        """
        Aktiviert die ganze Matrix mit der Ableitung der Sigmoid-Funktion

        Args:
            new_m (Matrix) = Neu erstellte Matrix mit den aktivierten Werten

        Returns:
            new_m (Matrix) = Die, mit der Ableitung der Sigmoid-Funktion, aktivierten Matrix
        """
        new_m = Matrix(self.rows, self.columns)
        for row in range(self.rows):
            for column in range(self.columns):
                sigmoid_value = self.data[row][column]
                new_m.data[row][column] = sigmoid_value * (1 - sigmoid_value)
        return new_m