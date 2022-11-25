import numpy as np


from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import FirefoxOptions

user = 'pixelizedgaming'
url = f'https://github.com/{user}'
width = 52
length = 39


# set up logger
class page_wrapper:
    def __init__(self):
        self.prev_frame = np.empty((length,width))
        opts = FirefoxOptions()
        self.browser = wd.Firefox(executable_path=r'geckodriver.exe',options=opts)
        self.browser.get(url)

        try:
            print("Waiting for page to load...")
            elem = WebDriverWait(self.browser, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "js-calendar-graph-svg")) 
        )
        finally:
            print("Loaded!")
            self.set_up_rects()

    
    def set_up_rects(self):
        if (self.browser == None):
             return
        calendar_element = self.browser.find_element_by_class_name('js-calendar-graph-svg')
        self.browser.execute_script("arguments[0].setAttribute('height',arguments[1])",calendar_element, (717/width*length)) # make sure the calendar frame is right size
        calendar = calendar_element.find_element_by_tag_name('g')
        cols = calendar.find_elements_by_tag_name('g')
        for x in range(len(cols)):
            row_list = cols[x].find_elements_by_css_selector("*")
            if (len(row_list) <= length):
                for i in range(len(row_list), length):
                    # Goofy ass implementation but fuck man Im not learning node just to make this run faster
                    script = f"""
                    console.log(arguments[0])
                    const rect = arguments[0].lastElementChild.cloneNode(true);
                    console.log(rect);
                    rect.setAttribute("x", (14-{x}));
                    rect.setAttribute("y", (13 * {i}));
                    arguments[0].appendChild(rect);
                    """
                    try:
                        self.browser.execute_script(script, cols[x])
                    except Exception as e:
                        print(e)
                        return False
        return True

    def display_image(self, image, frame):
        if (self.browser == None):
             return
        calendar_element = self.browser.find_element_by_class_name('js-calendar-graph-svg')
        calendar = calendar_element.find_element_by_tag_name('g')
        cols = calendar.find_elements_by_tag_name('g')
        for x in range(len(cols) - 1):
            for i in range(0, length):
                if image[i,x] == self.prev_frame[i,x]:
                    continue
                script = f"""
                const rect = arguments[0].children[{i}];
                rect.setAttribute("data-level", {image[i,x]});
                """
                try:
                    self.browser.execute_script(script, cols[x])
                except Exception as e:
                    print(e)
        self.browser.save_screenshot(f"images/frame{frame}.png")
        self.prev_frame = image
    



    