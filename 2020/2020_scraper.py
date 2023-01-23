from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup

driver = webdriver.Firefox(executable_path="./geckodriver.exe")
driver.maximize_window()
dataframe = pd.DataFrame(columns=["Title", "Company", "Location", "Salary", "Description"])

# Depending on how many pages return, set 100 to where the &start= value is on the last page and add 10
# e.g. if start ends at 170 for the last page, enter 180
for i in range(0, 100, 10):
    # Enter url of search here
    url = ""
    driver.get(url + "&start=" + str(i))
    driver.implicitly_wait(3)

    all_jobs = driver.find_elements_by_class_name('result')

    for job in all_jobs:

        result_html = job.get_attribute('innerHTML')
        soup = BeautifulSoup(result_html, 'html.parser')

        title = soup.find("a", class_="jobtitle").text.replace('\n', '')

        try:
            location = soup.find(class_="location").text
        except:
            location = 'None'

        try:
            company = soup.find(class_="company").text.replace("\n", "").strip()
        except:
            company = 'None'

        try:
            salary = soup.find(class_="salary").text.replace("\n", "").strip()
        except:
            salary = 'None'

        sum_div = job.find_elements_by_class_name("summary")[0]

        try:
            sum_div.click()
        except:
            close_button = driver.find_elements_by_class_name("popover-x-button-close")[0]
            close_button.click()
            sum_div.click()

        jd = driver.find_element_by_css_selector('div#vjs-desc').text

        dataframe = dataframe.append({'Title': title,
                                      "Company": company,
                                      'Location': location,
                                      "Salary": salary,
                                      "Description": jd},
                                     ignore_index=True)

dataframe.to_csv("dataset.csv", index=False)
