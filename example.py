def find_resulting_number(number: int) -> int:
    current_number = square(number=number)
    current_number = multiply_by_two(number=current_number)
    current_number = subtract_ten(number=current_number)
    return current_number


def square(number: int) -> int:
    return number ** 2


def multiply_by_two(number: int) -> int:
    return number * 2


def subtract_ten(number: int) -> int:
    return number - 10
