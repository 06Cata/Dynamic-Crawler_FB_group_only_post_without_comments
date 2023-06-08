from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import csv

# # 到 selenium # #
# 【零、設置好登入條件】
FACEBOOK_ID = "catalinakuowork@gmail.com"
FACEBOOK_PW = "Aa_0954033969"
TARGET_URL = "https://www.facebook.com/groups/pythontw"


# 【一、創建瀏覽器、指定無痕模式】
options = webdriver.ChromeOptions()
options.add_argument("incognito")


# 【二、創建 Chrome 瀏覽器的 webdriver 實例，打開 url】
# print 出頁面的標題
driver = webdriver.Chrome(options = options)
driver.get("https://www.facebook.com")


# 【三、使用 find_element() 找到要輸入的表格】
email =  driver.find_element(By.ID, "email")
password = driver.find_element(By.ID, "pass")
login = driver.find_element(By.NAME, "login")

# 【三-二、輸入零、的資料, 送出】
email.send_keys(FACEBOOK_ID)
password.send_keys(FACEBOOK_PW)
login.submit()

time.sleep(3)



# # 到 beautifulsoup # #
#【一、取得網頁內容】
# 要求get url
driver.get(TARGET_URL)

time.sleep(3)


# 【一-二、設置js滾動滑鼠的次數】
for x in range(1, 10):
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(5)


#【一-三、HTML 內容轉換為 BeautifulSoup 物件】
soup = BeautifulSoup(driver.page_source, 'html.parser')


# 【二、找出所有文章時間+部分文章, 寫進迴圈。開啟 CSV 檔案並準備寫入】
times = soup.findAll("a", {"class": "x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g xt0b8zv xo1l8bm"})
titles = soup.findAll("span", {"class": "x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u x1yc453h"})
print("一共:" + str(len(titles)) + " 則文章...")


#'a' 是增加進去,  'w'是覆蓋
with open('news.csv', 'a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # 寫入表頭
    writer.writerow(['時間', '標題'])
    
    # 寫入每篇文章的時間和內容(X打開顯示更多的)
    for i in range(len(titles)):
        # 取得時間內容, 有可能讀不到, 設置try except
        try:
            time_text = times[i].text
        except IndexError:
            continue

        # 取得文章內容
        title_text = titles[i].text
        blank = "--------------------------------------"

        # 寫入資料到 CSV 檔案
        writer.writerow([time_text])
        writer.writerow([title_text])
        writer.writerow([blank])


        # 順便印出來看看
        print("時間:", time_text)
        print("標題:", title_text)
        print("----------------------------------------")


#【三、關閉瀏覽器】
driver.quit()
