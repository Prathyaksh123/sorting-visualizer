import random

def generate_array(size, min_val, max_val):
    """
    Generates a random array of integers.

    Args:
        size (int): Number of elements in the array.
        min_val (int): Minimum value of an element.
        max_val (int): Maximum value of an element.

    Returns:
        list: A list containing random integers.
    """
    return [random.randint(min_val, max_val) for _ in range(size)]
