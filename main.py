from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from constants import brand_map
from datetime import datetime
import time


def get_total_page(driver):
    try:
        pages = driver.find_element(By.CLASS_NAME, "pager")
    except:
        pages = None
        print("0 items in this brand")
    if not pages:
        return 1
    else:
        total_page = pages.find_elements(By.CLASS_NAME, "pagerNum")[-1].text
        try:
            total_page = int(total_page)
            return total_page
        except Exception as e:
            print("can not find total page" + e)  

def get_elements(table):
    td_elements = table.find_elements(By.TAG_NAME, 'td')
    return [element.text if element.text else "" for element in td_elements]



def main():
    time_t = time.time()
    # 初始化 WebDriver
    driver = webdriver.Chrome()  # 如果 chromedriver 不在系统路径中，可以指定路径，如 webdriver.Chrome('/path/to/chromedriver')

    count = 0
    #查找每一个牌子的车
    for key, maker in brand_map.items():
        #初始化 DataFrame
        df = pd.DataFrame(columns=["値段", "年式", "走行距離", "排気量", "車検", "修復歴", "地域"])
        
        #计时
        time_b = time.time()

        # 打开目标网页首页
        driver.get(f'https://kakaku.com/kuruma/used/spec/Maker={key}')
        
        # 找到总页数
        total_page = get_total_page(driver=driver)
        for i in range(1, total_page + 1):
            page = i
            driver.get(f'https://kakaku.com/kuruma/used/spec/Maker={key}/Page={page}')
            try:
                contents= driver.find_elements(By.CLASS_NAME,'-total')
                prices = [content.text for content in contents] # 获取这页的价格
                tables = driver.find_elements(By.CLASS_NAME, "p-specTable2_body")
                assert len(prices) == len(tables)
                for i in range(len(prices)):
                    elements = get_elements(tables[i])
                    elements = [prices[i]] + elements
                    df.loc[len(df)] = elements
            except Exception as e:
                print(e)
        print("success: " + maker)
        print("cost time is: " + str(time.time() - time_b))
        if count == 0:
            with pd.ExcelWriter('output_v2.xlsx', engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name=maker, index=False)
        else:
            with pd.ExcelWriter('output_v2.xlsx', engine='openpyxl', mode='a', if_sheet_exists='new') as writer:
                df.to_excel(writer, sheet_name=maker, index=False)
        count = count + 1
    
    print("total brands are: " + str(count))
    print("total cost time is: " + str(time.time() - time_t))
    input("Press Enter to close the browser...")
    

if __name__ == "__main__":
    main()