from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd


def scrape ():
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

#Mars News
url = 'https://redplanetscience.com/'
browser.visit(url)
browser.is_element_present_by_css('div.list_text', wait_time=1)
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')
slide_elem.find('div', class_='content_title')
news_title = slide_elem.find('div', class_='content_title').get_text()
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()




#Featured Image
url1 = 'https://spaceimages-mars.com/'
browser.visit(url1)
html1 = browser.html
news_soup1 = soup(html1, 'html.parser')
slide_elem1 = news_soup1.select_one('div.floating_text_area')
image_url_location = slide_elem1.find('a')
image_url= image_url_location['href']
featured_image_url= (f'{url1}{image_url}')
featured_image_url



#Mars Facts
url2 = 'https://galaxyfacts-mars.com/'
tables = pd.read_html(url2)
tables_df= tables[0]
tables_df=tables_df.rename(columns={0:'Description', 1:'Mars', 2:'Earth'})
tables_df.set_index('Description')
tables_df.to_html("Mars Facts.html")



#Mars Hemispheres
url3= ['https://marshemispheres.com/cerberus.html', 'https://marshemispheres.com/schiaparelli.html', 'https://marshemispheres.com/syrtis.html', 'https://marshemispheres.com/valles.html']
browser.visit('https://marshemispheres.com/cerberus.html')
html3 = browser.html

news_soup3 = soup(html3, 'html.parser')

slide_elem3 = news_soup3.select_one('img.wide-image')

slide_elem3['src']
slide_elem4 = news_soup3.select_one('div', class_='cover')
slide_elem4.h2.text

titles_img=[]

for item in url3:
    browser.visit(item)
    html3 = browser.html

    news_soup3 = soup(html3, 'html.parser')

    slide_elem3 = news_soup3.select_one('img.wide-image')
    slide_elem4 = news_soup3.select_one('div', class_='cover')

    list1=[slide_elem4.h2.text, slide_elem3['src']]
    titles_img.append(list1)


hemisphere_image_url=[]
for title, img in titles_img:
    hemisphere_dict={'Title':title, 'img_url': img}
    hemisphere_image_url.append(hemisphere_dict)