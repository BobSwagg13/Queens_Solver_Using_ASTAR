from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from algo import solve
import re
from concurrent.futures import ThreadPoolExecutor
import time

def js_click(driver, element):
    driver.execute_script("arguments[0].click();", element)
    
def click_cell(cell):
    try:
        cell.click()
        cell.click()
    except Exception as e:
        print(f"Click failed: {e}")

def solve_web():
    driver = webdriver.Chrome()
    driver.get("https://www.linkedin.com/games/queens")

    wait = WebDriverWait(driver, 10)

    # Wait for iframe and switch
    iframe = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".game-launch-page__iframe")))
    driver.switch_to.frame(iframe)

    # Start game
    start_button = wait.until(EC.element_to_be_clickable((By.ID, "launch-footer-start-button")))
    start_button.click()

    # Close pop-up
    close_button = wait.until(EC.element_to_be_clickable((By.ID, "ember61")))
    close_button.click()

    # Wait for game cells to appear
    cells = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".queens-cell-with-border")))

    # Prepare matrix and cell map
    cell_data = []
    cell_map = {}
    max_row = 0
    max_col = 0

    for cell in cells:
        # Get both attributes efficiently via JS
        class_attr, aria_label = driver.execute_script(
            "return [arguments[0].className, arguments[0].getAttribute('aria-label')];", cell
        )

        color_match = re.search(r'cell-color-(\d+)', class_attr)
        pos_match = re.search(r'row (\d+), column (\d+)', aria_label)

        if color_match and pos_match:
            color = int(color_match.group(1))
            row = int(pos_match.group(1)) - 1
            col = int(pos_match.group(2)) - 1

            cell_data.append((row, col, color))
            cell_map[(row, col)] = cell
            max_row = max(max_row, row)
            max_col = max(max_col, col)

    # Build matrix for solver
    matrix = [[None for _ in range(max_col + 1)] for _ in range(max_row + 1)]
    for row, col, color in cell_data:
        matrix[row][col] = color

    # Solve!
    result = solve(matrix)

    # Click all solution cells directly!
    with ThreadPoolExecutor(max_workers=8) as executor:
        executor.map(lambda coord: click_cell(cell_map.get(tuple(coord))), result)

    for coordinate in result:
        matrix[coordinate[0]][coordinate[1]] = 'O'

    for row in matrix:
        print(row)
    input("Press Enter to close the browser...")
    driver.quit()
