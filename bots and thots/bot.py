from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from utility_methods.utility_methods import *
import urllib.request 
import os
import time

import configparser


class InstaBot:

    def __init__(self,username=None,password=None):
        """
        Initialize instance of InstagramBot class. 

        Call the login method to authenticate user with IG.
        Args:
            username:str: The User on Instagram, specified or read from config
            password:str: Insta password for user, specified or read from config

        Attributes: 
            drive_path: str: Path to chromedriver(.exe)
            driver: Selenium.webdriver.Chrome: Chromedriver automates browser actions
            login_url:str:Url to IG Login
            nav_user_url:str:go to homepage
            get_tag_url:str: Url search posts with a hashtag
            logged_in:bool: Boolean logged in
        """
        self.username=config['IG_AUTH']['USERNAME']
        self.password=config['IG_AUTH']['PASSWORD']
        self.login_url=config['IG_URLS']['LOGIN']
        self.nav_user_url=config['IG_URLS']['NAV_USER']
        self.get_tag_url=config['IG_URLS']['SEARCH_TAGS']
        self.base_url='https://www.instagram.com/'
        
        self.driver=webdriver.Chrome(config['ENVIRONMENT']['CHROMEDRIVER_PATH'])
        self.logged_in=false
        #self.driver = webdriver.Chrome(ChromeDriverManager().install())
        #self.driver=webdriver.Chrome('chromedriver.exe')
        #self.driver.get('https://www.instagram.com/')
        self.login()

        #self.base_url='https://www.instagram.com/'

    @insta_method
    def login(self):
        """
            Login User to web portal
        """
        self.driver.get(self.login_url)
        
        #self.driver.get('{}/accounts/login/'.format(self.base_url))
        
        #self.driver.find_element_by_name('username').sendkeys(self.username)
        #self.driver.find_element_by_name('password').sendkeys(self.password)
        login_btn=self.driver.find_elements_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[3]')
        #login is 4th element of this div array
        

        username_input=self.driver.find_element_by_name('username')
        password_input=self.driver.find_element_by_name('password')

        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        login_btn.click()
        #time.sleep(2)


    @insta_method
    def search_tag(self,tag):
        """
        Navigates to search for posts with a certain hashtag

        Args:
            tag:str:Tag to search for
        """
        self.driver.get(self.get_tag_url.format(tag))


    @insta_method
    def nav_user(self,user):
        """
        Naviages to user profile
        Args: 
            user:str: Username to navigate to
        """
        self.driver.get(self.nav_user_url.format(user))
        #self.driver.get('https://instagram.com/mischifffashion')
        

    @insta_method
    def user_follow_action(self,user,unfollow=False):
        if unfollow==True:
            action_button_text='Following'



    @insta_method
    def follow_user(self,user):
        """
        Follows user(s)
        Args:
            user:str: Username of user to follow
        """
        self.nav_user(user)
        follow_buttons=self.find_buttons('Follow')
        for btn in follow_buttons:
            btn.click()
        #follow_buttons=follow_text_element_list=self.driver.find_elements_by_xpath("//button[contains(text()','Follow')]")[0]
        #follow_button.click()
        #follow_text_element_list[0].click()
        #print(follow_text_element_list)
        #print(len(follow_text_element_list))

    
    @insta_method
    def unfollow_user(self, user):
        """
        Unfollows user(s)

        Args:
            user:str: Username of user to unfollow
        """
        self.nav_user(user)
        unfollow_btns=self.find_buttons('Following')

        if unfollow_btns:
            for btn in unfollow_btns:
                btn.click()
                unfollow_confirmation=self.find_buttons('Unfollow')[0]
                unfollow_confirmation.click()
        else:
            print('No {} buttons found'.format('Following'))


    @insta_method
    def download_user_images(self,user):
        """
        Downloads all images from users profile
        """
        self.nav_user(user)
        img_srcs=[]
        finished=False
        while not finished:
            finished=self.infinite_scroll() #scroll down

            img_srcs.extend([img.get_attribute('src') for img in self.driver.find_elements_by_class_name('FFVAD')])  #scrapes the sources
            img_srcs=list(set(img_srcs)) #scrape duplicates


        for idx, src in enumerate(img_srcs):
            self.download_image(src,idx,user)



    @insta_method
    def like_latest_posts(self,user,n_posts,like=True):
        """
        Likes a number of a users latest posts, specified by n


        Args:
            user:str: User whose posts to like or unlike
            n_posts:int: Number of recent posts to like or unlike
            like:bool: If True, likes recent posts, else if False unlikes recent posts

        """
        action='Like' if like else 'Unlike'

        self.nav_user(user)
        imgs=[]
        imgs.extend(self.driver.find_elements_by_class_name('_9AhH0'))


        for img in imgs[:n_posts]:
            img.click()
            time.sleep(1)
            try:
                self.driver.find_element_by_xpath("//*[@aria-label='{}']".format(action)).click()
            except Excetion as e:
                print(e)

            #self.comment_post('beep boop testing bot')
            self.driver.find_elements_by_class_name('ckWGn')[0].click()



    #@insta_method
    #def comment_post(self, text):
        #"""
        #Comments on a post that is in modal form
        #"""

        #comment_input = self.driver.find_elements_by_class_name('Ypffh')[0]
        #comment_input.click()
        #comment_input.send_keys(text)
        #comment_input.send_keys(Keys.Return)

        #print('Commentd.')



    def download_image(self, src, image_filename,folder):
        """
        Creates folder named after user to store image, downloads to folder 
        """
        folder_path='./{}'.format(folder)
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)

        img_filename='image_{}.jpg'.formate(image_filename)
        urllib.request.urlretrieve(src,'{}/{}'.format(folder,img_filename))


    def infinite_scroll(self):
        """
        Scrolls to bottom of user page to load aggregate media

        Returns:
            bool: True if bottom page is reached, false etherwise
        """

        SCROLL_PAUSE_TIME=1

        self.last_height=self.driver.execute_script("return document.body.scrollHeight")
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)

        self.new_height = self.driver.execute_script("return document.body.scrollHeight")


        if self.new_height == self.last_height:
            return True

        self.last_height = self.new_height
        return False


def find_buttons(self, button_text):
        """
        Finds buttons for following and unfollowing users by filtering follow elements for buttons. Defaults to finding follow buttons.
        Args:
            button_text: Text that the desired button(s) has 
        """

        buttons = self.driver.find_elements_by_xpath("//*[text()='{}']".format(button_text))

        return buttons


if __name__ == '__main__':

    config_file_path = './config.ini' 
    logger_file_path = './bot.log'
    config = init_config(config_file_path)
    logger = get_logger(logger_file_path)

    bot = InstaBot()
    bot.login()

    bot.like_latest_posts('mischifffashion', 2, like=True)
