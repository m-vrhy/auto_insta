from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import os 
import time
import configparser


class InstagramBot:

    # Method to scroll through browser
    def scroll(self):
        SCROLL_PAUSE_TIME = .5

    # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    #Initialize with username, password, and login to Instagram.com
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.base_url = 'https://www.instagram.com/'
        self.driver = webdriver.Chrome('./chromedriver.exe')
        self.login()


        
    #Enters username and password then signs in
    def login(self):
        self.driver.get('{}accounts/login/'.format(self.base_url))
        time.sleep(1)
        username_input=self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[2]/div/label/input')
        username_input.click()
        username_input.send_keys(self.username)

        password_input=self.driver.find_element_by_name('password')
        password_input.click()
        password_input.send_keys(self.password)
        
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]/button/div').click()
        
        time.sleep(2)

    # Navigates to a users page given the username
    def nav_user(self, user):
        self.driver.get('{}{}/'.format(self.base_url, user))
    
    # Navigates to a users page and follows
    def follow_user(self, user):
        self.nav_user(user)
        
        follow_button = self.driver.find_elements_by_xpath("//button[contains(text(), 'Follow')]")[0]
        follow_button.click()

    # Likes all the posts on a single page
    def like_all_posts(self, url):
        self.driver.get(url)
        self.scroll()
        posts = self.driver.find_elements_by_class_name("v1Nh3")
        for post in posts:
            post.click()
            time.sleep(1)
            try:
                self.driver.find_element_by_xpath("//span[@class=\"glyphsSpriteHeart__outline__24__grey_9 u-__7\" and @aria-label=\"Like\"]//parent::button").click()
                time.sleep(1)
                self.driver.find_element_by_xpath("//button[@class=\"ckWGn\"]").click()
            except:
                self.driver.find_element_by_xpath("//button[@class=\"ckWGn\"]").click()   

    # Goes to the explore page for a given term and comments on x amount of posts.
    def comment_from_explore(self,  search_term, num_of_posts, comment):
        comment = str(comment)
        if num_of_posts > 33:
            num_of_posts = 33
        
        self.driver.get('{}{}/tags/{}/'.format(self.base_url, "explore", search_term))
        #don't scroll so comments go on top posts
        time.sleep(1)

        posts=self.driver.find_elements_by_class_name('v1Nh3')[9:9+num_of_posts]
        
        for post in posts:
            print(post)
            post.click()
            time.sleep(1)
    
            #send to text receiver
            text_receiver = self.driver.find_element_by_class_name('Ypffh')
            text_receiver.click()
            time.sleep(1)#sleep so text receiver becomes visible
            
            text_receiver = self.driver.find_element_by_class_name('Ypffh')#reassign to avoid StaleElementReferenceException
            text_receiver.send_keys(comment)
            text_receiver.send_keys(Keys.RETURN)
            self.driver.find_element_by_xpath("//button[@class=\"ckWGn\"]").click()   

    # Comments on each post on a profile.
    def comment_on_profile(self, username, num_of_posts, comment):
        self.nav_user(username)
        posts = self.driver.find_elements_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div/div[1]/div[1]')[9:num_of_posts]
        for post in posts:
        
            post.click()
            time.sleep(1)
    
            #send to text receiver
            text_receiver = self.driver.find_element_by_class_name('Ypffh')
            text_receiver.click()
            time.sleep(1)#sleep so text receiver becomes visible
            
            text_receiver = self.driver.find_element_by_class_name('Ypffh')#reassign to avoid StaleElementReferenceException
            text_receiver.send_keys(comment)
            text_receiver.send_keys(Keys.RETURN)
            self.driver.find_element_by_xpath("//button[@class=\"ckWGn\"]").click()



if __name__ == '__main__':
    print("Starting...")
    # Initialize a class using --> ig_bot = InstagramBot('USERNAME', 'PASSWORD')

    # Here you can call any methods on class to get started!  


