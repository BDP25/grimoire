import math


class Calculator:
    def add(self, a: float, b: float) -> float:
        return a + b

    def subtract(self, a: float, b: float) -> float:
        return a - b

    def multiply(self, a: float, b: float) -> float:
        return a * b

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b


class Geometry:
    def area_circle(self, radius: float) -> float:
        return math.pi * radius**2

    def perimeter_circle(self, radius: float) -> float:
        return 2 * math.pi * radius

    def area_rectangle(self, length: float, width: float) -> float:
        return length * width

    def perimeter_rectangle(self, length: float, width: float) -> float:
        return 2 * (length + width)


def factorial(n: int) -> int:
    if n < 0:
        raise ValueError("Factorial not defined for negative numbers")
    if n in {0, 1}:
        return 1
    result: int = 1
    for i in range(2, n + 1):
        result *= i
    return result


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    return all(n % i != 0 for i in range(2, int(math.sqrt(n)) + 1))


def fibonacci(n: int) -> list[int]:
    if n <= 0:
        raise ValueError("Input must be a positive integer")
    sequence: list[int] = [0, 1]
    for _ in range(n - 2):
        sequence.append(sequence[-1] + sequence[-2])
    return sequence[:n]


def reverse_string(s: str) -> str:
    return s[::-1]


def count_vowels(s: str) -> int:
    vowels: str = "aeiouAEIOU"
    return sum(1 for char in s if char in vowels)
