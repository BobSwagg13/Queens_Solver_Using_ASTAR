from parser import parse
from algo import solve
from clicker import solve_web
import os

def main():
    while True:
        type = input("TXT or WEB(LinkedIn puzzle)?: ")
        if type == "TXT":
            file_path = input("Enter file path: ")
            if not os.path.exists(file_path):
                print("File not found!")
                continue
            matrix = parse(file_path)
            result = solve(matrix)

            for coordinate in result:
                matrix[coordinate[0]][coordinate[1]] = "O"

            for row in matrix:
                print(row)
        elif type == "WEB":
            solve_web()
        elif type == "EXIT":
            break
        else:
            print("Please enter WEB, TXT, or EXIT to exit!")


if __name__ == "__main__":
    main()
