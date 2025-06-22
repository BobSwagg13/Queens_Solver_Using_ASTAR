import heapq


class Area:
    def __init__(self, id, list_of_coordinates):
        self.id = id
        self.list_of_coordinates = list_of_coordinates  # [[1, 2],[2, 3]]
        self.size = len(list_of_coordinates)


class Board_state:
    def __init__(self, board, list_of_areas, step):
        self.board = board
        self.list_of_areas = list_of_areas
        self.filled_count = 0
        self.row = len(board)
        self.col = len(board[0])
        self.step = step

    def get_area_id(self, coordinate):
        """Returns area id based on coordinates"""
        try:
            for area in self.list_of_areas:
                if coordinate in area.list_of_coordinates:
                    return area.id
        except:
            print("Coordinates out of bounds!")

    def place_queen(self, coordinate):
        """Adds queen to board as well as blocks the next invalid placements"""

        if not self.is_valid_placement(coordinate):
            return

        area_id = self.get_area_id(coordinate)
        if not self.is_valid_area(area_id):
            heapq.heappop(self.list_of_areas)

        # Fills x and y of the coordinate with X
        for i in range(self.col):
            self.board[coordinate[0]][i] = "X"
        for j in range(self.row):
            self.board[j][coordinate[1]] = "X"

        # Fills around the coordinate with X
        if coordinate[0] > 0 and coordinate[1] > 0:
            self.board[coordinate[0] - 1][coordinate[1] - 1] = "X"

        if coordinate[0] < self.row - 1 and coordinate[1] > 0:
            self.board[coordinate[0] + 1][coordinate[1] - 1] = "X"

        if coordinate[0] > 0 and coordinate[1] < self.col - 1:
            self.board[coordinate[0] - 1][coordinate[1] + 1] = "X"

        if coordinate[0] < self.row - 1 and coordinate[1] < self.col - 1:
            self.board[coordinate[0] + 1][coordinate[1] + 1] = "X"

        area = self.get_area(area_id)
        for coor in area.list_of_coordinates:
            self.board[coor[0]][coor[1]] = "X"

        self.board[coordinate[0]][coordinate[1]] = "Q"

    def is_valid_area(self, area_id) -> bool:
        """Checks if areas is full by X"""
        area = self.get_area(area_id)
        coor_x_count = 0

        for coor in area.list_of_coordinates:
            if self.board[coor[0]][coor[1]] == "X":
                coor_x_count += 1
        return coor_x_count <= area.size

    def is_valid_placement(self, coordinate) -> bool:
        """Checks valid placement of coordinate on board"""
        for i in range(self.row):
            if self.board[coordinate[0]][i] == "Q":
                return False
        for i in range(self.col):
            if self.board[i][coordinate[1]] == "Q":
                return False

        if (
            self.board[coordinate[0]][coordinate[1]] == "Q"
            or self.board[coordinate[0]][coordinate[1]] == "X"
        ):
            return False

        return True

    def is_valid_board(self) -> bool:
        """Checks if every area on board is valid"""
        for area in self.list_of_areas:
            if not self.is_valid_area(area.id):
                return False

        return True

    def is_finish(self) -> bool:
        """Checks if board is finish state"""
        for row in self.board:
            if row.count("X") == self.col or row.count(" ") > 0:
                return False

        for area in self.list_of_areas:
            if not self.is_valid_area(area.id):
                return False
        return True

    def set_filled_count(self) -> int:
        """Updates filled count"""
        total = 0
        for row in self.board:
            total += row.count(" ")
        self.filled_count = self.col * self.row - (total)

    def get_queen_count(self) -> int:
        """Returns number of queen on current board"""
        total = 0
        for row in self.board:
            total += row.count("Q")
        return total

    def get_area(self, area_id) -> Area:
        """Returns area object by id"""
        for area in self.list_of_areas:
            if area.id == area_id:
                return area
        return None

    def get_queen_coordinates(self) -> list[list[int]]:
        """Returns the current queen coordinates"""
        queens = []
        for i in range(self.row):
            for j in range(self.col):
                if self.board[i][j] == "Q":
                    queens.append([i, j])

        return queens

    def __lt__(self, other):
        """Comparison rule for prioqueue"""
        return self.filled_count + self.step > other.filled_count + other.step
        