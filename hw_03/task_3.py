class MatrixHashMixin:
    def __hash__(self):
        # just sum of all numbers in matrix (remainder of divide by 100, hash shouldn't be too big)
        hash_value = 0
        for row in self.matrix:
            for element in row:
                hash_value += hash(element)
        return hash_value % 100
    
    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return self.matrix == other.matrix

class Matrix(MatrixHashMixin):
    _matmul_cache = {}
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
        hashed_pair = (hash(self),hash(other))
        if (hashed_pair in self._matmul_cache): # if already calculated, just return cached value
            return self._matmul_cache[hashed_pair]
        mtx = []
        for i in range(self.rows):
            row = []
            for j in range(other.cols):
                row.append(sum(self.matrix[i][k] * other.matrix[k][j] for k in range(self.cols)))
            mtx.append(row)

        self._matmul_cache[hashed_pair] = Matrix(mtx) # save multiplication in cache
        return Matrix(mtx)
    
    def _is_valid(self, matrix):
        if not all(len(row) == self.cols for row in matrix):
            raise ValueError("rows have different length")
    
    
    def __str__(self):
        max_len = [max(len(str(row[i])) for row in self.matrix) for i in range(self.cols)]
        return_string = "\n".join(" ".join(str(element).ljust(max_len[i]) for i, element in enumerate(row)) for row in self.matrix)

        return return_string
    
    @staticmethod
    def write_matrix_to_file(matrix, filename):
        with open(filename, 'w') as file:
            for row in str(matrix):
                file.write(row)
if __name__ == "__main__":
    A = Matrix([[1, 1], [1, 2]])
    B = Matrix([[3, 4], [8, 10]])
    C = Matrix([[5, 0], [0, 0]])
    D = Matrix([[3, 4], [8, 10]])

    Matrix.write_matrix_to_file(A, 'artifacts/task_3/A.txt')
    Matrix.write_matrix_to_file(B, 'artifacts/task_3/B.txt')
    Matrix.write_matrix_to_file(C, 'artifacts/task_3/C.txt')
    Matrix.write_matrix_to_file(D, 'artifacts/task_3/D.txt')

    # verify conditions
    assert hash(A) == hash(C)  
    assert A != C 
    assert B == D

    AB_matmul = A @ B
    Matrix._matmul_cache = {}
    CD_matmul = C @ D

    Matrix.write_matrix_to_file(AB_matmul, 'artifacts/task_3/AB.txt')
    Matrix.write_matrix_to_file(CD_matmul, 'artifacts/task_3/CD.txt')
    with open('artifacts/task_3/hash.txt', "w") as file:
        file.write(f"A@B hash: {hash(AB_matmul)}\nC@D hash: {hash(CD_matmul)}") # print true hash of matmul (without caching)
    
    assert (AB_matmul != CD_matmul)