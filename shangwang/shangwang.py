from selenium import webdriver
import time
from apscheduler.schedulers.blocking import BlockingScheduler
import sys

def logout(driver):
    driver.get('http://10.4.1.17:81/')
    driver.find_element_by_css_selector('tbody>tr>td>a').click()


def login(driver):
    try:
        driver.get('http://10.4.1.17/')
        driver.find_element_by_css_selector('#username').send_keys('zhang.chen3')
        driver.find_element_by_css_selector('#password').send_keys('Alang34925//')
        driver.find_element_by_css_selector('tbody>tr:nth-child(3)>td:nth-child(3)').click()
    except:
        login(driver)


def main():
    option = webdriver.ChromeOptions()
    option.add_argument('--start-maximized')
    driver = webdriver.Chrome('d:/chromedriver.exe', chrome_options=option)
    driver.set_page_load_timeout(5)
    try:
        logout(driver)
        print('退出登录成功')
    except:
        print('已经退出登录，不必再退出')
    else:
        time.sleep(3)
    login(driver)
    driver.close()
    print('登录成功')


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('定时任务开始执行')
        scheduler = BlockingScheduler()
        scheduler.add_job(main, 'cron', day_of_week='0-6', hour=0, minute=10)
        scheduler.start()
    elif sys.argv[1] == 'debug':
        print("debug模式运行")
        main()
