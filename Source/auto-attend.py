import time
import schedule
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
# manages needed libraries


def login():  # logs into Canvas and opens all classes
    driver = get_driver()

    driver.get("http://lms.pps.net")

    driver.find_element_by_name("pseudonym_session[password]").send_keys(login_info[1])
    driver.find_element_by_name("pseudonym_session[unique_id]").send_keys(login_info[0])
    # logs in

    time.sleep(3)
    counter = 1

    while True:  # clicks all class links then closes the program when no more are found
        try:
            link = driver.find_element_by_xpath(f'//*[@id="DashboardCard_Container"]/div/div[{str(counter)}]/div/a/div/h3/span')
            course_title = link.text
            link.click()
            driver.implicitly_wait(10)

            log = course_title + "; " + str(datetime.now())
            print(log)

            f = open("history.log", "a")
            f.write(log + "\n")
            f.close()

            time.sleep(3)
            driver.find_element_by_class_name("ic-icon-svg--dashboard").click()
            driver.implicitly_wait(10)

            counter += 1

        except NoSuchElementException:
            print("Ended Session: " + str(datetime.now()))
            driver.quit()
            break

        except Exception as e:
            log = "Error: " + str(e) + "; " + str(datetime.now())

            f = open("history.log", "a")
            f.write(log + "\n")
            f.close()


def get_driver():  # creates web driver

    options_driver = Options()
    options_driver.add_argument("--log-level=3")
    options_driver.add_argument("--headless")
    # defines extra driver options

    driver = webdriver.Chrome(executable_path="chromedriver.exe", options=options_driver)
    # creates the web driver

    return driver


print("Running program...\nDo not close")

f = open("login.txt", "r")
login_info = f.readlines()
f.close()
# gets login information

f = open("times.txt", "r")
time_info = f.readlines()
f.close()
# gets times for the program to login to classes

open("history.log", "w").close()
# clears the history.log file


print("\nTimes:")
for t in time_info:
    t = t.rstrip("\n")
    print(t)

    schedule.every().day.at(t.rstrip("\n")).do(login)

while True:  # checks if it is time to login
    schedule.run_pending()
    time.sleep(1)