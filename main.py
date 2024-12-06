
def scrape_page(url):
    driver = webdriver.Chrome()  # Make sure you've installed the ChromeDriver
    driver.get(url)


    # Deena

    # Function to extract a date from text using regex
    # Matches dates like "31 March 2023"
    def extract_date_from_text(text):
        date_pattern = r'\b\d{1,2} \w+ \d{4}\b'
        match = re.search(date_pattern, text)
        if match:
            return match.group()  # Return the first matched date
        return None

    # Method to return the Return Date
    def get_return_date(driver):
        paragraphs = driver.find_elements(By.TAG_NAME, "p")
        for paragraph in paragraphs:
            if "prepared on" in paragraph.text:
                return extract_date_from_text(paragraph.text)
        return "Not Found"

    # Method to return the Last Reviewed Date
    def get_last_reviewed_date(driver):
        paragraphs = driver.find_elements(By.TAG_NAME, "p")
        for paragraph in paragraphs:
            if "last reviewed on" in paragraph.text:
                return extract_date_from_text(paragraph.text)
        return "Not Found"

    # Method to return the Last Tested Date
    def get_last_tested_date(driver):
        paragraphs = driver.find_elements(By.TAG_NAME, "p")
        for paragraph in paragraphs:
            if "last tested on" in paragraph.text:
                return extract_date_from_text(paragraph.text)
        return "Not Found"


    # Extract data - placeholders
    data = {
        "URL": url,
          "Date Prepared By": get_return_date(driver),
          "Date Last Reviewed": get_last_reviewed_date(driver),
          "Date Last Tested": get_last_tested_date(driver),
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
        url = row['Statement URL']
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

