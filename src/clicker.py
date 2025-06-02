from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from algo import solve
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import re


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

    iframe = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".game-launch-page__iframe"))
    )
    driver.switch_to.frame(iframe)

    # Start game
    start_button = wait.until(
        EC.element_to_be_clickable((By.ID, "launch-footer-start-button"))
    )
    start_button.click()

    # Close pop-up
    close_button = wait.until(EC.element_to_be_clickable((
        By.CSS_SELECTOR, 'button[aria-label="Dismiss"]'
    )))
    close_button.click()

    # Wait for game cells to appear
    cells = wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, ".queens-cell-with-border")
        )
    )

    # Prepare matrix and cell map
    cell_data = []
    cell_map = {}
    max_row = 0
    max_col = 0

    # Parse data
    for cell in cells:
        class_attr, aria_label = driver.execute_script(
            "return [arguments[0].className, arguments[0].getAttribute('aria-label')];",
            cell,
        )

        color_match = re.search(r"cell-color-(\d+)", class_attr)
        pos_match = re.search(r"row (\d+), column (\d+)", aria_label)

        if color_match and pos_match:
            color = int(color_match.group(1))
            row = int(pos_match.group(1)) - 1
            col = int(pos_match.group(2)) - 1

            cell_data.append((row, col, color))
            cell_map[(row, col)] = cell
            max_row = max(max_row, row)
            max_col = max(max_col, col)

    matrix = [[None for _ in range(max_col + 1)] for _ in range(max_row + 1)]
    for row, col, color in cell_data:
        matrix[row][col] = color

    result = solve(matrix)

    # Click all solution cells!
    with ThreadPoolExecutor(max_workers=8) as executor:
        executor.map(lambda coord: click_cell(cell_map.get(tuple(coord))), result)

    date_str = datetime.now().strftime("%Y-%m-%d")

    file_name = f"test/LinkedIn_puzzle_{date_str}.txt"

    with open(file_name, "w") as f:
        for i in range(max_row):
            for j in range(max_col):
                f.write(str(matrix[i][j]))
            if i < max_row - 1:
                f.write("\n")

    for coordinate in result:
        matrix[coordinate[0]][coordinate[1]] = "O"

    for row in matrix:
        print(row)
    input("Press Enter to close the browser...")
    driver.quit()
