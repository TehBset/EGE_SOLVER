import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time
from dearpygui.dearpygui import *

if __name__ == '__main__':
    def main_body(url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        questions = soup.find_all('div', class_='prob_view')
        driver = webdriver.Edge(EdgeChromiumDriverManager().install())
        driver.get(url)
        driver.maximize_window()
        anwsers = []
        for i in range(len(questions)):
            link = str(questions[i].find('a')).split('"')
            anwsers.append(find_qu_ans('https://chem-ege.sdamgia.ru' + link[1]))
        fields = driver.find_elements_by_class_name("prob_view")
        i = 0
        for field in fields:
            form = field.find_element_by_class_name("test_inp")
            form.click()
            form.send_keys(anwsers[i])
            i += 1
        driver.find_element_by_css_selector("input[type='button']").click()
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, 470)")
        driver.save_screenshot("SCREENSHOT.png")
        time.sleep(60)
        driver.close()


    def find_qu_ans(url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        soluition = soup.find('div', class_='solution')
        soluition = soluition.find_all('p')
        soluition = str(soluition[len(soluition) - 1])
        ans = ''
        for i in soluition:
            if i.isdigit():
                ans += i
        return ans[1:]


    create_context()
    create_viewport()
    setup_dearpygui()
    set_viewport_width(720)
    set_viewport_height(360)
    set_viewport_title('SOLVER')
    set_viewport_resizable(False)
    set_viewport_large_icon('logo.ico')
    set_viewport_small_icon('logo.ico')


    def save_callback():
        main_body(str(get_value("link")))


    with window(label="MAIN_MENU", height=360, width=720, no_close=True, no_collapse=True, no_resize=True, no_move=True,
                no_title_bar=True):
        add_text("1.Create a link to the test from the nth number of tasks and paste it here.")
        add_text("2.After the bot passes everything, you will have 60 seconds to screenshot the results.")
        add_text("3.The bot will automatically create a screenshot and save it to the program folder.")
        link = add_input_text(label="URI", tag="link")
        add_button(label="RUN", callback=save_callback)
    show_viewport()
    start_dearpygui()
    destroy_context()
