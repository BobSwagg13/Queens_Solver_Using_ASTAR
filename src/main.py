from parser import parse
from algo import Area, Board_state, solve
from clicker import solve_web
 
def main():

    while True:
        type = input("TXT or WEB?: ")
        if(type == "TXT"):
            file_path = input("Enter file path: ")
            matrix = parse(file_path)
            result = solve(matrix)

            for coordinate in result:
                matrix[coordinate[0]][coordinate[1]] = 'O'

            for row in matrix:
                print(row)
        elif(type == "WEB"):
            solve_web()
        elif(type == "EXIT"):
            break
        else:
            print("Please enter WEB, TXT, or EXIT to exit!")



    

    
            
                
    
    

    


if __name__ == "__main__":
    main()