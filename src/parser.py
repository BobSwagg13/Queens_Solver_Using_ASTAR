def parse(filepath) -> list[list[int]]:
    """Parse from txt"""
    matrix = []
    with open(filepath, "r") as file:
        for line in file:
            row = [int(char) for char in line.strip()]
            matrix.append(row)

    return matrix
