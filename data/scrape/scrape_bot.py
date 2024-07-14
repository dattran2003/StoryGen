from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import os
import sys
import shutil

import os.path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


class SStruyen:
    def __init__(self):
        ##### Setup #####        
        chrome_options = Options()
        # chrome_options.add_argument("--headless") # Ensure GUI is off
        chrome_options.add_argument("--no-sandbox")

        homedir = os.path.expanduser("~")
        chrome_options.binary_location = f"{homedir}/chrome-linux64/chrome"
        webdriver_service = Service(f"{homedir}/chromedriver-linux64/chromedriver")
        ##################

        self.driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
        self.driver.get("https://sstruyen.vn/")

    def find_search_bar(self):
        return self.driver.find_element(By.NAME, 'search')  

    def search_books_by_keyword(self, search_key, filter=None):
        search_bar = self.find_search_bar()  
        search_bar.send_keys(search_key)
        search_bar.send_keys(Keys.RETURN)
        time.sleep(2)

        book_container = self.driver.find_element(By.CLASS_NAME, 'book-list')
        table = book_container.find_element(By.TAG_NAME, 'table')
        trs = table.find_elements(By.TAG_NAME, 'tr')   

        books = []

        for tr in trs:
            h3 = tr.find_element(By.TAG_NAME, 'h3')
            book_title = h3.text

            if(filter):
                if(filter in book_title):
                    books.append(book_title) 
            else:
                books.append(book_title)
        # self.driver.back()
        return books

    def get_chapter_title(self):
        chapter_div = self.driver.find_element(By.CSS_SELECTOR, 'div.row.list-chap')
        # chapter_div.find_elements() 

        lis = chapter_div.find_elements(By.TAG_NAME, 'li')

        chapters = []
        for li in lis:
            chap = li.text
            chapters.append(chap)

        return chapters    

    def save_chapter(self, dir, title, content):
        file_path = f'{dir}/{title}.txt'
        with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
                print(f'{file_path}')

    def scrape_chapter(self):
        content_div = self.driver.find_element(By.CSS_SELECTOR, 'div.content.container1') 
        return content_div.text
    
    def scrape_chapters_in_page(self, dir):
        chapters = self.get_chapter_title()

        for chap_title in chapters:
            a = self.driver.find_element(By.LINK_TEXT, chap_title)
            a.click()
            content = self.scrape_chapter()
            self.save_chapter(dir, chap_title, content)
            self.driver.back()

    def scrape_chapters_in_pages(self, dir):
        self.scrape_chapters_in_page(dir)
        
        
        while(True):
            li = self.driver.find_element(By.CLASS_NAME, 'next')
            next_button = li.find_element(By.TAG_NAME, 'a')
            if(next_button.get_attribute('href')[-1] == '#'):
                break
            next_button.click()
            self.scrape_chapters_in_page(dir)

        
    def scrape_book_by_title(self, dir, title): 
        search_bar = self.find_search_bar()
        search_bar.send_keys(title[:20])
        search_bar.send_keys(Keys.RETURN)

        a = self.driver.find_element(By.LINK_TEXT, title) 
        a.click()
        self.scrape_chapters_in_pages(dir)

if __name__=='__main__':
    ss = SStruyen()
    books = ss.search_books_by_keyword('Hậu Cuốn Theo Chiều Gió')     
    print(books)   

    dir = '/home/tandattran772/persional_project/StoryGen/data/raw/'
    for title in books:
        path = f'{dir}/{title}'
        os.mkdir(path)
        # title = title[:-9]
        ss.scrape_book_by_title(path,title)
        
        break
