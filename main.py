from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Start a new instance of Chrome
driver = webdriver.Chrome()

# Navigate to TradingView
driver.get("https://www.tradingview.com/chart/?symbol=BITSTAMP%3ABTCUSD")

parameters_to_optimize = {
    'smaShort': range(5, 25),
    'smaLong': range(10, 45),
    # add other parameters here
}

import itertools

# Define a function to apply parameters and retrieve performance using Selenium
def apply_parameters_and_get_performance(driver, params):
    try:
        # Navigate to the strategy settings pane.
        # Note: The actual button ID/class/name and navigation steps need to be determined
        # by inspecting the TradingView web page.
        settings_button = driver.find_element(By.ID, 'settings_button_id')
        settings_button.click()

        # Example of setting a parameter (this will depend on the actual HTML structure)
        # and assuming we're setting a moving average length as an example parameter
        ma_length_input = driver.find_element(By.ID, 'ma_length_input_id')
        ma_length_input.clear()
        ma_length_input.send_keys(str(params['moving_avg_length']))

        # Apply/OK button click after setting parameters
        apply_button = driver.find_element(By.ID, 'apply_button_id')
        apply_button.click()

        # Navigate to the strategy report section
        # [Note]: This and subsequent selectors need to be updated per actual webpage structure
        report_button = driver.find_element(By.ID, 'report_button_id')
        report_button.click()

        # Extract the ROI or other metric from the report
        # This assumes that the ROI is simply displayed in a certain element after running the strategy.
        # In practice, extracting this data might involve navigating a results table, handling loading delays, etc.
        roi_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'roi_element_id'))
        )
        roi = float(roi_element.text.replace('%', ''))

        return roi
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None
    pass

# Get all possible combinations of parameters
all_parameter_combinations = itertools.product(*parameters_to_optimize.values())

best_roi = -float('inf')
best_params = None

# Loop through all parameter combinations
for param_combination in all_parameter_combinations:
    params = dict(zip(parameters_to_optimize.keys(), param_combination))
    
    # Apply parameters and get performance using Selenium
    roi = apply_parameters_and_get_performance(driver, params)
    
    # Update the best parameters if this combination is better
    if roi > best_roi:
        best_roi = roi
        best_params = params
