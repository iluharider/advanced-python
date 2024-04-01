import numpy as np

class Matrix:
    def __init__(self, matrix):
        self.matrix = matrix
        self.rows = len(matrix)
        self.cols = len(matrix[0])
        self._is_valid(matrix)

    def __add__(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("The matrices have different dimensions and cannot be added.")
        mtx = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                row.append(self.matrix[i][j] + other.matrix[i][j])
            mtx.append(row)

        return Matrix(mtx)

    def __mul__(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("invalid matrix sizes for this operation")
        
        mtx = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                row.append(self.matrix[i][j] * other.matrix[i][j])
            mtx.append(row)
        return Matrix(mtx)
    
    def __matmul__(self, other):
        if self.cols != other.rows:
            raise ValueError("invalid matrix sizes for this operation")
        mtx = []
        for i in range(self.rows):
            row = []
            for j in range(other.cols):
                row.append(sum(self.matrix[i][k] * other.matrix[k][j] for k in range(self.cols)))
            mtx.append(row)
        return Matrix(mtx)
    
    def _is_valid(self, matrix):
        if not all(len(row) == self.cols for row in matrix):
            raise ValueError("rows have different length")
    
    
    def __str__(self):
        max_lengths = [max([len(str(row[i])) for row in self.matrix]) for i in range(self.cols)]

        table_str = ""
        for row in self.matrix:
            for i, element in enumerate(row):
                table_str += str(element).ljust(max_lengths[i]) + " "
            table_str += "\n"

        return table_str
    
    @staticmethod
    def write_matrix_to_file(matrix, filename):
        with open(filename, 'w') as file:
            for row in str(matrix):
                file.write(row)


if __name__ == "__main__":
    np.random.seed(0)
    matrix1 = Matrix(np.random.randint(0, 10, (10, 10)))
    matrix2 = Matrix(np.random.randint(0, 10, (10, 10)))

    result_addition = matrix1 + matrix2
    result_multiplication = matrix1 * matrix2
    result_matrix_multiplication = matrix1 @ matrix2

    

    Matrix.write_matrix_to_file(result_addition, 'artifacts/matrix+.txt')
    Matrix.write_matrix_to_file(result_multiplication, 'artifacts/matrix*.txt')
    Matrix.write_matrix_to_file(result_matrix_multiplication, 'artifacts/matrix@.txt')