from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
browser = webdriver.Chrome()
browser.get('https://www.crimemapping.com/map/agency/64')
when_btn = browser.find_element_by_class_name('viewWhen')
when_btn.click()
time.sleep(1)
previous_4_weeks_btn = browser.find_elements_by_css_selector('div[style="width:100%; cursor:pointer"]')[3]
previous_4_weeks_btn.click()
time.sleep(1)
reports_btn = browser.find_element_by_class_name('viewReportToolbar')
reports_btn.click()
time.sleep(4)
dic = {'Description':[],'Incident#':[],'Location':[],'Agency':[],'Date':[]}
c_row = {'Description':[],'Incident#':[],'Location':[],'Agency':[],'Date':[]}
data = pd.DataFrame()
for i in range(24):
    soup = bs(browser.page_source,'html.parser')
    l = soup.findAll('tr', {'role':'row'})
    rows = l[1:]
    for row in rows:
        cl = row.findChildren('td',recursive=False)
        c_row['Description'] = cl[2].text
        c_row['Incident#'] = cl[3].text
        c_row['Location'] = cl[4].text
        c_row['Agency'] = cl[5].text
        c_row['Date'] = cl[6].text
        data = data.append(c_row,ignore_index = True)
    next_button = browser.find_element_by_css_selector('a.k-link[title="Go to the next page"]')
    next_button.click()
    time.sleep(1)
data.to_csv('crime_data.csv')
browser.close()
