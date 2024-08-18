import requests
import bs4
from selenium import webdriver
from selenium.webdriver.common.by import By

def main():

    # 初始化 WebDriver
    driver = webdriver.Chrome()  # 如果 chromedriver 不在系统路径中，可以指定路径，如 webdriver.Chrome('/path/to/chromedriver')

    # 打开目标网页
    driver.get('https://kakaku.com/kuruma/used/')

    # 通过 ID 查找按钮元素，并模拟点击
    try:
        button = driver.find_element(By.CLASS_NAME,'btn')  # 用实际的按钮 ID 替换 'button-id'
        button.click()
        print("Button clicked successfully!")
        input("Press Enter to close the browser...")
    except Exception as e:
        print(f"Failed to click the button: {e}")

    # 关闭浏览器
    # driver.quit()
    

if __name__ == "__main__":
    main()