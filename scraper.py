import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By


def prompt_position(position):
    position = input("Enter a job position: ")
    return position


def prompt_location(location):
    location = input("Enter a location (City, State or Zip or remote): ")
    return location


def get_url(position, location):
    url_template = "https://www.indeed.com/jobs?q={}&l={}"
    url = url_template.format(position, location)
    return url


def main(position, location):
    position = prompt_position(position)
    location = prompt_location(location)
    url = get_url(position, location)
    dataframe = pd.DataFrame(columns=["Title", "Company", "Location", "Salary", "Description"])

    # Ensure that the driver path is correct before running this script.

    # Microsoft Windows
    # driver_path = "./drivers/windows/geckodriver.exe"

    # Linux
    driver_path = "./drivers/linux/geckodriver"

    driver = webdriver.Firefox(executable_path=driver_path)

    postings = 110

    for i in range(0, postings, 10):
        driver.get(url + "&start=" + str(i))
        driver.implicitly_wait(3)

        jobs = driver.find_elements(By.CLASS_NAME, 'job_seen_beacon')

        for job in jobs:
            result_html = job.get_attribute('innerHTML')
            soup = BeautifulSoup(result_html, 'html.parser')

            tb = soup.find('tbody')
            tr = tb.find('tr')
            t = tr.find_all('h2', {'class': 'jobTitle jobTitle-color-purple jobTitle-newJob'})

            for n in t:

                # Job Title
                job_title = n.find_all('span')[1].get_text()
                # print("Job Title: " + job_title)

                # Company
                find_company = soup.find('span', class_="companyName")
                if find_company:
                    company = find_company.get_text()
                    # print("Company: " + company)
                else:
                    company = 'None'
                    # print("Company: " + company)

                # Location
                find_job_location = soup.find('div', class_='companyLocation')
                if find_job_location:
                    job_location = find_job_location.get_text()
                    # print("Location: " + job_location)
                else:
                    job_location = 'None'
                    # print("Location: " + job_location)

                # Salary
                find_salary = soup.find('div', class_='metadata salary-snippet-container')
                if find_salary:
                    salary = find_salary.get_text()
                    # print("Salary: " + salary)
                else:
                    salary = 'None'
                    # print("Salary: " + salary)

                # Description
                find_description = soup.find('div', class_='job-snippet')
                if find_description:
                    description = find_description.get_text()
                    # print("Description: " + description)
                else:
                    description = 'None'
                    # print("Description: " + description)

                # print('\n')

                # Add the job posts to the dataframe
                dataframe = dataframe.append({'Title': job_title,
                                              "Company": company,
                                              'Location': job_location,
                                              "Salary": salary,
                                              "Description": description},
                                             ignore_index=True)

    # Convert the dataframe to a csv file
    date = datetime.today().strftime('%Y-%m-%d')
    dataframe.to_csv(date + "_" + position + "_" + location + ".csv", index=False)
    driver.quit()


main('', '')
