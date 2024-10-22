import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
# define input path

input_path = "input.csv"  # Path to your CSV file with URLs
output_path = "output.csv"  # Path where you want to store the scraped data

# define output object & columns
output_columns = [
    "URL", "Date Prepared By", "Date Last Reviewed", "Date Last Tested",
    "Days Since Last Tested", "Who Tested By", "Feedback Header Present",
    "Reporting Problems Header Present", "Enforcement Procedure Header Present",
    "Compliance Status"
]
output_data = []

# iterate through input rows
def check_header_present(driver, header_text):
    try:
        header = driver.find_element(By.XPATH, f"//*[contains(text(), '{header_text}')]")
        return "Yes" if header else "No"
    except:
        return "No"


def scrape_page(url):
    driver = webdriver.Chrome()  # Make sure you've installed the ChromeDriver
    driver.get(url)

    #     get value y, save into output row object etc
    #         date prepared by
    #         date last reviewed
    #         date last tested
    #         days since last tested
    #         who tested by
    #         "Feedback and contact information" header present
    # 	      "Reporting accessibility problems" header present
    #         "Enforcement procedure" header present
    #         compliance status

    # Extract data - placeholders
    data = {
        "URL": url,
        # "Date Prepared By": date_prepared_by(),
        # "Date Last Reviewed": date_last_reviewed(),
        # "Date Last Tested": date_last_tested(),
        # "Days Since Last Tested": days_since_last_tested(),
        # "Who Tested By": who_tested_by(),
        "Feedback Header Present": check_header_present(driver, 'Feedback and contact information'),
        "Reporting Problems Header Present": check_header_present(driver, 'Reporting accessibility problems'),
        "Enforcement Procedure Header Present": check_header_present(driver, 'Enforcement procedure'),
        # "Compliance Status": compliance_status(),
    }

    driver.quit()  # Close the browser window
    return data


with open(input_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        url = row['URL']
        # Call a function to scrape the required data from the page

        scraped_data = scrape_page(url)
        #     add populated row to output
        output_data.append(scraped_data)
#     open url

# write output to correct location
with open(output_path, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=output_columns)
    writer.writeheader()
    writer.writerows(output_data)

print(output_data)


# Helper function to check if a header is present

# any cleanup