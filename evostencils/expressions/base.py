import abc
from operator import mul as builtin_mul
from functools import reduce


# Base classes
class Expression(abc.ABC):
    @property
    @abc.abstractmethod
    def shape(self):
        pass


class Entity(Expression):
    @property
    def name(self):
        return self._name

    @property
    def shape(self):
        return self._shape


class UnaryExpression(Expression):
    def __init__(self, operand):
        self._operand = operand
        self._shape = operand.shape

    @property
    def operand(self):
        return self._operand

    @property
    def shape(self):
        return self._shape


class BinaryExpression(Expression):
    @property
    def operand1(self):
        return self._operand1

    @property
    def operand2(self):
        return self._operand2

    @property
    def shape(self):
        return self._shape


# Entities
class Operator(Entity):
    def __init__(self, name, shape):
        self._name = name
        self._shape = shape


class Identity(Operator):
    def __init__(self, shape):
        super(Identity, self).__init__('I', shape)


class Zero(Operator):
    def __init__(self, shape):
        super(Zero, self).__init__('0', shape)


class Grid(Entity):
    def __init__(self, name, size):
        self._name = name
        self._shape = (size, 1)

    @property
    def size(self):
        return self._shape[0]


# Unary Expressions
class Diagonal(UnaryExpression):
    pass


class LowerTriangle(UnaryExpression):
    pass


class UpperTriangle(UnaryExpression):
    pass


class Inverse(UnaryExpression):
    pass


class Transpose(UnaryExpression):
    def __init__(self, operand):
        self._operand = operand
        self._shape = (operand.shape[1], operand.shape[0])


# Binary Expressions
class Addition(BinaryExpression):
    def __init__(self, operand1, operand2):
        assert operand1.shape == operand2.shape, "Operand shapes are not equal"
        self._operand1 = operand1
        self._operand2 = operand2
        self._shape = operand1.shape


class Subtraction(BinaryExpression):
    def __init__(self, operand1, operand2):
        assert operand1.shape == operand2.shape, "Operand shapes are not equal"
        self._operand1 = operand1
        self._operand2 = operand2
        self._shape = operand1.shape


class Multiplication(BinaryExpression):
    def __init__(self, operand1, operand2):
        assert operand1.shape[1] == operand2.shape[0], "Operand shapes are not aligned"
        self._operand1 = operand1
        self._operand2 = operand2
        self._shape = (operand1.shape[0], operand2.shape[1])


# Scaling
class Scaling(Expression):
    def __init__(self, factor, operand):
        self._factor = factor
        self._operand = operand
        self._shape = operand.shape

    @property
    def factor(self):
        return self._factor

    @property
    def operand(self):
        return self._operand

    @property
    def shape(self):
        return self._shape


# Wrapper functions
def inv(operand):
    return Inverse(operand)


def add(operand1, operand2):
    return Addition(operand1, operand2)


def sub(operand1, operand2):
    return Addition(operand1, operand2)


def mul(operand1, operand2):
    return Multiplication(operand1, operand2)


def scale(factor, operand):
    return Scaling(factor, operand)


def generate_grid(name: str, grid_size: tuple) -> Grid:
    n = reduce(builtin_mul, grid_size, 1)
    return Grid(name, n)


def generate_operator(name: str, grid_size: tuple) -> Operator:
    n = reduce(builtin_mul, grid_size, 1)
    return Operator(name, (n, n))