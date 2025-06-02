import heapq
import copy
from parser import parse
from board import Area, Board_state


def solve(matrix):
    row_length = len(matrix)
    col_length = len(matrix[0])

    # Get area count of current board
    area_count = 0
    for i in matrix:
        mx = max(i)
        if mx > area_count:
            area_count = mx

    area_count += 1
    areas = [[] for _ in range(area_count)]

    # Gets the coordinates for each area and make it as an object
    for i in range(row_length):
        for j in range(col_length):
            areas[matrix[i][j]].append([i, j])

    new_areas = []
    for i in range(len(areas)):
        area = Area(i, areas[i])
        new_areas.append(area)

    new_areas.sort(key=lambda x: x.size, reverse=False)

    blank_board = [[" " for j in range(col_length)] for i in range(row_length)]
    pq = []

    heapq.heappush(pq, Board_state(blank_board, new_areas, 0))

    found = False
    while len(pq) > 0:
        current_board_state = heapq.heappop(pq)
        isFinished = current_board_state.is_finish()
        if isFinished:
            found = True
            break
        queen_count = current_board_state.get_queen_count()
        area = current_board_state.list_of_areas[queen_count]
        for coor in area.list_of_coordinates:
            if current_board_state.is_valid_placement(coor):
                new_board = copy.deepcopy(current_board_state.board)
                new_areas = copy.deepcopy(current_board_state.list_of_areas)
                new_state = Board_state(
                    new_board, new_areas, current_board_state.step + 1
                )
                new_state.place_queen(coor)
                if new_state.is_valid_board:
                    new_state.set_filled_count()
                    heapq.heappush(pq, new_state)

    if not found:
        print("No Solution")
        return []
    else:
        return current_board_state.get_queen_coordinates()
