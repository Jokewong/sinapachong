
# coding: utf-8

# In[4]:


import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup

def getNewsDetail(newsurl):
    result = {}
    res = requests.get(newsurl)
    res.encoding = 'utf-8'
    soup=BeautifulSoup(res.text, 'html.parser')
    timesource = soup.select('.date')[0].text
    result['title'] = soup.select('.main-title')[0].text
    result['newssource'] = soup.select('.date-source a')[0].text
    result['time'] = datetime.strptime(timesource, '%Y年%m月%d日 %H:%M')
    result['article'] = ' '.join([p.text.strip() for p in soup.select('#article p')[:-1]])
    result['editor'] = soup.select('.show_author')[0].text.strip('责任编辑：')
    return result
  
def parseListlinks(url):
    newsdetails = []
    res = requests.get(url)
    jd = json.loads(res.text.lstrip('  newsloadercallback(').rstrip(');'))
    for ent in jd['result']['data']:
        newsdetails.append(getNewsDetail(ent['url']))
    return newsdetails

url = 'http://api.roll.news.sina.com.cn/zt_list?channel=news&cat_1=gnxw&cat_2==gdxw1||=gatxw||=zs-pl||=mtjj&level==1||=2&show_ext=1&show_all=1&show_num=22&tag=1&format=json&page={}&callback=newsloadercallback&_=1525529812805'
news_total = []
for i in range(1,3):
    newsurl = url.format(i)
    newsary = parseListlinks(newsurl)
    news_total.extend(newsary)

import pandas
df = pandas.DataFrame(news_total)
df.head

df.to_excel('news.xlsx')

