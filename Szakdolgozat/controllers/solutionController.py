from models.matrixProblems import Matrixproblems
from models.vectorProblems import Vectorproblems
from models.vectorspaceProblems import Vectorspaceproblems
class Solutioncontroller:
    def __init__(self):
        self.matrix_solver = Matrixproblems()
        self.vector_solver = Vectorproblems()
        self.vector_space_solver=Vectorspaceproblems()


    def solver_handler(self,type,*args):
        """
        Egy dinamikus megoldas kezelo fuggveny, ami eldonti nev alapjan,
        hogy melyik solver file melyik solver fuggveny segitsegevel szamolja ki az adott problemakat
        :param type: problema neve pl. ("matrix_sum")
        :param args: problematol fuggoen, a parameterek a megoldas kiszamitasahoz
        """
        match type:

        #matrix solver kiválasztása
            case 'matrix_sum':
                self.matrix_solver.matrix_sum(*args)

            case 'matrix_mult':
                self.matrix_solver.matrix_mult(*args)

            case 'matrix_transpose':
                self.matrix_solver.matrix_transpose(*args)

            case 'matrix_invert':
                self.matrix_solver.matrix_invert(*args)

            case 'matrix_determinant':
                self.matrix_solver.matrix_determinant(*args)

            case 'matrix_cramer':
                self.matrix_solver.matrix_cramer(*args)

        #vektor solver kiválasztása

            case 'vector_norm':
                self.vector_solver.vector_norm(*args)

            case 'vector_sum':
                self.vector_solver.vector_sum(*args)

            case 'vector_mult':
                self.vector_solver.vector_mult(*args)

            case 'vector_linear_combination':
                self.vector_solver.vector_linear_combination(*args)

            case 'vector_scalar_mult':
                self.vector_solver.vector_scalar_mult(*args)

            case 'vectorial_mult':
                self.vector_solver.vectorial_mult(*args)

            case 'triangle_solution':
                self.vector_solver.triangle_solution(*args)

        #vektor terek solver kiválasztása

            case 'vector_spaces':
                self.vector_space_solver.vector_spaces(*args)

            case 'linear_independence':
                self.vector_space_solver.linear_independence(*args)

            case 'bases':
                self.vector_space_solver.bases(*args)

            case 'base_transformation':
                self.vector_space_solver.base_transformation(*args)

            case 'matrix_rank':
                self.vector_space_solver.matrix_rank(*args)

            case 'linear_equations':
                self.vector_space_solver.linear_equations_solver(*args)
