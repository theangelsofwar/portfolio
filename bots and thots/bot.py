from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import os
import time

import configparser


class InstagramBot:

    def __init__(self,username,password):
        """
        Initialize instance of InstagramBot class. 

        Call the login method to authenticate user with IG.
        Args:
            username:str: The User on Instagram
            password:str: Insta password for user

        Attributes: 
            driver: Selenium.webdriver.Chrome: Chromedriver automates browser actions
        """
        self.username=username
        self.password=password
        self.base_url='https://www.instagram.com/'
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        #self.driver=webdriver.Chrome('chromedriver.exe')
        #self.driver.get('https://www.instagram.com/')
        self.login()

        self.base_url='https://www.instagram.com/'

    def login(self):
        self.driver.get('{}/accounts/login/'.format(self.base_url))
        
        self.driver.find_element_by_name('username').sendkeys(self.username)
        self.driver.find_element_by_name('password').sendkeys(self.password)
        self.driver.find_elements_by_xpath("//div[contains(text(),'Log In')]")[0].click()
        
        
    def nav_user(self,user):

        self.driver.get('{}/{}'.format(self.base_url,user))
        
        self.driver.get('https://instagram.com/mischifffashion')
        
    def follow_user(self,user):
        self.nav_user(user)

        follow_button=self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[2]/div/span/span[1]/button')
        follow_button.click()



if __name__ == '__main__' :
  
    config_path= './config.ini'
    cparser=configparser.ConfigParser()
    cparser.read(config_path)
    username=cparser['AUTH']['USERNAME']
    password=cparser['AUTH']['PASSWORD']

    ig_bot=InstagramBot(username,password)
    print(ig_bot.username)
    # ig_bot.nav_user('mischifffashion')
    ig_bot.follow_user('mischifffashion')