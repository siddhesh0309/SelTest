import os, glob, shutil, datetime, pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import sleep
import xlwings as xw
from string import punctuation


def start_selenium_automation(from_date=None, to_date=None):
    try:
        xw_app = xw.App()
        xw_app.visible = False
        time_based_subfolder = "AMFI_Performance_Reports" + datetime.datetime.strftime(
            datetime.datetime.now(), "%d%m%Y_%H%M%S"
        )
        download_directory = os.path.join(os.getcwd(), time_based_subfolder)

        if not os.path.exists(download_directory):
            os.makedirs(download_directory)

        options = Options()
        options.add_argument("--ignore-certificate-errors")
        options.add_experimental_option(
            "prefs",
            {
                "download.default_directory": download_directory,
                "download.directory_upgrade": True,
            },
        )

        def call_for_date(driver, date):
            driver.find_element(
                By.XPATH, "//html[1]/body[1]/form[1]/div/div[1]/div[5]/div/input"
            ).clear()
            driver.find_element(
                By.XPATH, "//html[1]/body[1]/form[1]/div/div[1]/div[5]/div/input"
            ).send_keys(date)
            driver.find_element(
                By.XPATH, "//html[1]/body[1]/form[1]/div/div[1]/div[5]/div/input"
            ).send_keys(Keys.ENTER)

            print(f"Downloading for {date}")
            for header in headers_list:
                if header == "Open-ended":
                    for i in range(len(entities_list)):
                        try:
                            sleep(3)
                            driver.find_element(
                                By.XPATH,
                                "/html/body/form/div/div/div[2]/div[1]/div[1]/button",
                            ).click()
                            sleep(3)
                            driver.find_element(
                                By.XPATH,
                                "/html/body/div[2]/div/ul/li["
                                + str(i + 1)
                                + "]/a/span[1]",
                            ).click()
                            for j in range(len(sub_entities_list)):
                                try:
                                    driver.find_element(
                                        By.XPATH,
                                        "/html/body/form/div/div/div[3]/div[1]/div[1]/button",
                                    ).click()
                                    driver.find_element(
                                        By.XPATH,
                                        "/html/body/div[2]/div/ul/li["
                                        + str(j + 1)
                                        + "]/a",
                                    ).click()
                                    driver.find_element(
                                        By.XPATH, "//button[@type='submit']"
                                    ).click()
                                    sleep(2.5)
                                    if (
                                        not "data is unavailable"
                                        in driver.find_element(
                                            By.XPATH, ".//div[@id='performance-data']"
                                        ).text
                                    ):
                                        driver.find_element(
                                            By.XPATH,
                                            ".//a[@id='download-report-excel']",
                                        ).click()
                                        sleep(4)
                                        files = glob.glob(download_directory + "/*")
                                        max_file = max(files, key=os.path.getmtime)
                                        filename = max_file.split("/")[-1].split(".")[0]
                                        if "fund-performance" in filename:
                                            try:
                                                new_filename = (
                                                    header
                                                    + "--"
                                                    + entities_list[i]
                                                    + "--"
                                                    + sub_entities_list[j].translate(
                                                        str.maketrans(
                                                            "", "", punctuation
                                                        )
                                                    )
                                                    + "--"
                                                    + date
                                                    + ".xlsx"
                                                )
                                                new_path = max_file.replace(
                                                    filename,
                                                    header
                                                    + "--"
                                                    + entities_list[i]
                                                    + "--"
                                                    + sub_entities_list[j].translate(
                                                        str.maketrans(
                                                            "", "", punctuation
                                                        )
                                                    )
                                                    + "--"
                                                    + date,
                                                )
                                                os.rename(max_file, new_path)
                                                wb = xw_app.books.open(new_path)
                                                wb.save(new_filename)
                                                wb.close()
                                                shutil.move(
                                                    new_filename, download_directory
                                                )
                                                os.remove(new_path)
                                            except Exception as e:
                                                print(e)
                                except Exception as e:
                                    pass
                        except Exception as e:
                            pass

        link = "https://www.amfiindia.com/research-information/other-data/mf-scheme-performance-details"
        service = Service(
            "C:/Users/SIDDHESH/OneDrive/Desktop/HSBC DOC/chromedriver-win64/chromedriver.exe"
        )
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(link)
        WebDriverWait(driver, 40).until(
            EC.presence_of_all_elements_located((By.XPATH, "//iframe"))
        )
        iframe = driver.find_element(By.XPATH, "//iframe")
        driver.switch_to.frame(iframe)
        entity = driver.find_elements(
            By.XPATH, "/html/body/form/div/div/div[2]/div[1]/div[1]/select/option"
        )
        categories = driver.find_elements(
            By.XPATH, "/html/body/form/div/div/div[3]/div[1]/div[1]/select/option"
        )
        funds = driver.find_elements(
            By.XPATH, "/html/body/form/div/div/div[4]/div[1]/div[1]/select/option"
        )
        headers = driver.find_elements(
            By.XPATH, "//html/body/form/div/div/div[1]/div[1]/div[1]/select/option"
        )
        global entities_list, sub_entities_list, headers_list, Funds_data
        entities_list = []
        sub_entities_list = []
        Funds_data = []
        headers_list = []

        for i in headers:
            if i.get_attribute("text") != "Select Type":
                headers_list.append(i.get_attribute("text"))
        for i in funds:
            Funds_data.append(i.get_attribute("text"))
        for i in entity:
            if i.get_attribute("text") != "Select Category":
                entities_list.append(i.get_attribute("text"))
        for i in categories:
            if i.get_attribute("text") != "Sub Category":
                sub_entities_list.append(i.get_attribute("text"))

        if (
            len(headers) == 0
            or len(entities_list) == 0
            or len(sub_entities_list) == 0
            or len(Funds_data) == 0
        ):
            driver.close()
            raise Exception("Failed to fetch options from the website.")

        print("Connected to AMFI")
        site_calender = []
        start_date = driver.find_element(
            By.XPATH, "/html/body/form/div/div[1]/div[5]/div"
        ).get_attribute("data-date-start-date")
        end_date = driver.find_element(
            By.XPATH, "/html/body/form/div/div[1]/div[5]/div"
        ).get_attribute("data-date-end-date")

        for i in pd.date_range(start_date, end_date):
            site_calender.append(datetime.datetime.strftime(i, "%d-%m-%Y"))

        if from_date and to_date:
            daterange = pd.date_range(
                pd.to_datetime(from_date, dayfirst=True),
                pd.to_datetime(to_date, dayfirst=True),
                freq="D",
            )
            user_dates = [datetime.datetime.strftime(i, "%d-%m-%Y") for i in daterange]
            if (
                from_date in site_calender
                and to_date in site_calender
                and from_date < to_date
            ):
                for date in user_dates:
                    call_for_date(driver, date)
            else:
                raise Exception("Invalid date range provided.")
        else:
            user_dates = [
                driver.find_element(
                    By.XPATH, "//html[1]/body[1]/form[1]/div/div[1]/div[5]/div/input"
                ).get_attribute("value")
            ]
            for date in user_dates:
                call_for_date(driver, date)

        driver.close()
        xw_app.kill()
        return "Download completed successfully."

    except Exception as e:
        xw_app.kill()
        raise Exception(f"Error occurred: {str(e)}")
