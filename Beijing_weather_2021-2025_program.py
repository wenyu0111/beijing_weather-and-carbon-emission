from selenium import webdriver
from selenium.webdriver.common.by import By
from lxml import etree
import csv
import time
from pathlib import Path

#Selenium
def getWeather(url):
    weather_info = []
    
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(2)  

    try:
        button = driver.find_element(By.CLASS_NAME, value="lishidesc2")
        button.click()
        time.sleep(4)  
    except Exception as e:
        print(f"No much data available：{url}")

    page_source = driver.page_source
    resp_html = etree.HTML(page_source)
    resp_list = resp_html.xpath('//ul[@class="thrui"]/li')

#get weather info
    for li in resp_list:
        day_weather_info = {}
        day_weather_info['date_time'] = li.xpath('./div[1]/text()')[0].split(' ')[0]
        high = li.xpath('./div[2]/text()')[0]
        day_weather_info['high'] = high[:high.find('℃')]
        low = li.xpath('./div[3]/text()')[0]
        day_weather_info['low'] = low[:low.find('℃')]
        day_weather_info['weather'] = li.xpath('./div[4]/text()')[0]
        weather_info.append(day_weather_info)

    driver.quit()
    return weather_info

#mean process
weathers = []
for year in range(2021, 2026): 
    for month in range(1, 13):
        weather_time = f'{year}{month:02d}'
        url = f'https://lishi.tianqi.com/beijing/{weather_time}.html'
        print(f"crawling：{url}")
        weather = getWeather(url)
        weathers.extend(weather)

print(f"data count: {len(weathers)}")

#download to desktop
desktop_path = Path.home() / "Desktop"
file_path = desktop_path / "beijing_weather_2021_2025.csv"

print(f"\n✅ downloading：{file_path}")
with open(file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["date", "highest_temp", "lowest_temp", "weather"])
    writer.writerows([list(day_weather_dict.values()) for day_weather_dict in weathers])

print(f"\n✅ finished, data count: {len(weathers)}")
