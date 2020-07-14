from selenium import webdriver
from config import config
import time
import os
from pyvirtualdisplay import Display


class ExtractHtml:
    def __init__(self):
        """
        when the service is up, we start the browser and add extension to it and start the vpn connection
        """
        self.default_config = config["branch"]()
        self.display = Display(visible=0, size=(800, 600))
        self.display.start()
        self.browser = self.get_browser_obj_with_ext(ext_path=self.default_config.ext_path,
                                                     chrome_path=self.default_config.chrome_path)

    def restart_vpn(self):
        """
        closes the existing driver and restarts the driver
        :return:
        """
        self.browser.close()
        self.browser = self.get_browser_obj_with_ext(ext_path=self.default_config.ext_path,
                                                     chrome_path=self.default_config.chrome_path)

    def get_browser_obj_with_ext(self, ext_path, chrome_path):
        """
        return the browser object after adding extension
        :param ext_path: path to extension file
        :param chrome_path: path to chrome driver
        :return: browser object
        """
        option = webdriver.ChromeOptions()
        path = os.path.dirname(os.path.abspath(__file__)) + "/" + ext_path
        chrome_path = os.path.dirname(os.path.abspath(__file__)) + "/" + chrome_path
        option.add_extension(extension=path)
        option.add_argument("--start-maximized")
        option.add_argument('--no-sandbox')
        option.add_argument('--disable-dev-shm-usage')
        browser = webdriver.Chrome(options=option, executable_path=chrome_path)
        browser.get('chrome-extension://ffbkglfijbcbgblgflchnbphjdllaogb/cyberghost.html')
        time.sleep(2)
        python_button = browser.find_element_by_class_name("button")
        python_button.click()
        time.sleep(2)

        return browser

    def health_check(self):
        return {"status_code": 200, "message": "Container service running"}


    def page_getter(self, url_link):
        """
        return the html content of a given url
        :param url_link: url that needs to be scraped
        :return: html dump
        """
        try:
            self.browser.get(url=url_link)
        except Exception as e:
            print(str(e))
            self.restart_vpn()

        html_content = self.browser.page_source
        return html_content


