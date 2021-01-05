import time
import schedule
import subprocess
import platform
import errno
import warnings
import os
from datetime import datetime
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.chrome import service, webdriver, remote_connection
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common import utils
# manages needed libraries


class HiddenChromeService(service.Service):  # creates hidden Chrome service object
    def start(self):
        try:
            cmd = [self.path]
            cmd.extend(self.command_line_args())

            if platform.system() == 'Windows':
                info = subprocess.STARTUPINFO()
                info.dwFlags = subprocess.STARTF_USESHOWWINDOW
                info.wShowWindow = 0  # SW_HIDE (6 == SW_MINIMIZE)
            else:
                info = None

            self.process = subprocess.Popen(
                cmd, env=self.env,
                close_fds=platform.system() != 'Windows',
                startupinfo=info,
                stdout=self.log_file,
                stderr=self.log_file,
                stdin=subprocess.PIPE)
        except TypeError:
            raise
        except OSError as err:
            if err.errno == errno.ENOENT:
                raise WebDriverException(
                    "'%s' executable needs to be in PATH. %s" % (
                        os.path.basename(self.path), self.start_error_message)
                )
            elif err.errno == errno.EACCES:
                raise WebDriverException(
                    "'%s' executable may have wrong permissions. %s" % (
                        os.path.basename(self.path), self.start_error_message)
                )
            else:
                raise
        except Exception as e:
            raise WebDriverException(
                "Executable %s must be in path. %s\n%s" % (
                    os.path.basename(self.path), self.start_error_message,
                    str(e)))
        count = 0
        while True:
            self.assert_process_still_running()
            if self.is_connectable():
                break
            count += 1
            time.sleep(1)
            if count == 30:
                raise WebDriverException("Can't connect to the Service %s" % (
                    self.path,))


class HiddenChromeWebDriver(webdriver.WebDriver):  # creates hidden Chrome webdriver
    def __init__(self, executable_path="chromedriver", port=0,
                options=None, service_args=None,
                desired_capabilities=None, service_log_path=None,
                chrome_options=None, keep_alive=True):
        if chrome_options:
            warnings.warn('use options instead of chrome_options',
                        DeprecationWarning, stacklevel=2)
            options = chrome_options

        if options is None:
            # desired_capabilities stays as passed in
            if desired_capabilities is None:
                desired_capabilities = self.create_options().to_capabilities()
        else:
            if desired_capabilities is None:
                desired_capabilities = options.to_capabilities()
            else:
                desired_capabilities.update(options.to_capabilities())

        self.service = HiddenChromeService(
            executable_path,
            port=port,
            service_args=service_args,
            log_path=service_log_path)
        self.service.start()

        try:
            RemoteWebDriver.__init__(
                self,
                command_executor=remote_connection.ChromeRemoteConnection(
                    remote_server_addr=self.service.service_url,
                    keep_alive=keep_alive),
                desired_capabilities=desired_capabilities)
        except Exception:
            self.quit()
            raise
        self._is_remote = False


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

            f = open("history.log", "a")
            f.write(log + "\n")
            f.close()

            time.sleep(3)
            driver.find_element_by_class_name("ic-icon-svg--dashboard").click()
            driver.implicitly_wait(10)

            counter += 1

        except NoSuchElementException:
            driver.quit()
            break

        except Exception as e:
            log = "Error: " + str(e) + "; " + str(datetime.now())

            f = open("history.log", "a")
            f.write(log + "\n")
            f.close()

            time.sleep(10)


def get_driver():  # creates web driver
    from selenium import webdriver

    options_driver = webdriver.ChromeOptions()
    options_driver.add_argument("headless")
    options_driver.add_argument("--silent")
    
    driver = HiddenChromeWebDriver(chrome_options=options_driver)

    return driver


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

for t in time_info:
    t = t.rstrip("\n")
    schedule.every().day.at(t.rstrip("\n")).do(login)

login()
# logs in initially when run

while True:  # checks if it is time to login
    schedule.run_pending()
    time.sleep(1)