import numpy as np

class MatrixMixin:
    def get_value(self, i, j):
        if (i > self.rows or i < 0 or j > self.cols or j < 0):
            raise ValueError("index is out of matrix sizes")
        return self.matrix[i][j]

    def set_value(self, i, j, value):
        if (i > self.rows or i < 0 or j > self.cols or j < 0):
            raise ValueError("index is out of matrix sizes")
        self.matrix[i][j] = value

    def __str__(self):
        max_len = [max(len(str(row[i])) for row in self.matrix) for i in range(self.cols)]
        return_string = "\n".join(" ".join(str(element).ljust(max_len[i]) for i, element in enumerate(row)) for row in self.matrix)

        return return_string
    
    def save_to_file(self, path):
        with open(path, 'w') as file:
            file.write(self.__str__() + '\n')
    
    def get_size(self):
        return (self.rows, self.cols)

class Matrix(MatrixMixin, np.lib.mixins.NDArrayOperatorsMixin):
    def __init__(self, matrix):
        self.matrix = matrix
        self.rows = len(matrix)
        self.cols = len(matrix[0])

        if not all(len(row) == self.cols for row in matrix):
            raise ValueError("rows have different length")
        
    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        out = kwargs.get('out', ())
        for x in inputs + out:
            if not isinstance(x, (Matrix,)):
                return NotImplemented

        inputs = tuple(x.matrix if isinstance(x, Matrix) else x for x in inputs)

        if out:
            kwargs['out'] = tuple(x.matrix if isinstance(x, Matrix) else x for x in out)

        result = getattr(ufunc, method)(*inputs, **kwargs)

        if type(result) is tuple:
            return tuple(type(self)(x) for x in result)
        
        elif method == 'at':
            return None
        
        else:
            return type(self)(result)

if __name__ == "__main__":

    np.random.seed(0)
    mtx_1 = Matrix(np.random.randint(0, 10, (10, 10)))
    mtx_2 = Matrix(np.random.randint(0, 10, (10, 10)))
        
    res1 = mtx_1 + mtx_2
    res2 = mtx_1 - mtx_2
    res3 = mtx_1 * mtx_2
    res4 = mtx_1 @ mtx_2

    res1.save_to_file("./artifacts/task_2/matrix+.txt")
    res2.save_to_file("./artifacts/task_2/matrix-.txt")
    res3.save_to_file("./artifacts/task_2/matrix_mul.txt")
    res4.save_to_file("./artifacts/task_2/matrix@.txt")

    # getters and setters usage
    print(f"matrix size: {mtx_1.get_size()}")
    print(f"Get value from (1,1): {mtx_1.get_value(1, 1)}")

    print("set value 10 at (1,1)")
    mtx_1.set_value(1, 1, 10)
    print(f"print setted value: {mtx_1.get_value(1, 1)}")
    