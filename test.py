from chalicelib import db_connect

import requests
from bs4 import BeautifulSoup
import datetime

def kp_seek_scrape():
    page = requests.get("http://www.nzkoreapost.com/bbs/board.php?bo_table=market_recruit")
    soup = BeautifulSoup(page.content, 'html.parser')

    table = soup.find_all('table', {'class': 'table div-table list-tbl bg-white'})
        
    l = []
    for items in table:
        for i in range(len(items.find_all('tr'))-1):
            data = {}
            if items.find_all('tr')[i].has_attr('class') == False:
                data['wr_id'] = items.find_all('tr')[i].find('td', class_='text-center font-11').span.get_text()
                data['title'] = items.find_all('tr')[i].find('td', class_='list-subject').a.strong.get_text()
                data['wrtier'] = items.find_all('tr')[i].find('td', class_='list-subject').div.find('span', class_='member').get_text()
                data['click_cnt'] = items.find_all('tr')[i].find('td', class_='text-center en').span.get_text().split(' ')[1]
                data['url'] = items.find_all('tr')[i].find('td', class_='list-subject').a['href']
                l.append(data)
    return l

#### TO-DO: insert only new advertisement and update 'click_cnt' if there is
def add_new_seek():
    scrapes = kp_seek_scrape()
    with db_connect.conn.cursor() as cur:
        sql_query = "SELECT * FROM users"
        cur.execute(sql_query)
        l = [row[0] for row in cur]
        print(scrapes.wr_id)
        if scrapes['wr_id'] in l:
          print(scrapes['wr_id'])
          


add_new_seek()