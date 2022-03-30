from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd
import datetime as dt

def scrape_all():
   # Initiate headless driver for deployment
   executable_path = {'executable_path': ChromeDriverManager().install()}
   browser = Browser('chrome', **executable_path, headless=True)
   news_title, news_paragraph = mars_news(browser)
   # Run all scraping functions and store results in a dictionary
   data = {
       "news_title": news_title,
       "news_paragraph": news_paragraph,
       "featured_image": featured_image(browser),
       "facts": mars_facts(),
       "hemispheres": mars_hemisphere(browser),
       "last_modified": dt.datetime.now()
   }
   # Stop webdriver and return data
   browser.quit()
   return data

def mars_news(browser):
   # Scrape Mars News
   # Visit the mars nasa news site
   url = 'https://redplanetscience.com/'
   browser.visit(url)
   # Optional delay for loading the page
   browser.is_element_present_by_css('div.list_text', wait_time=1)
   # Convert the browser html to a soup object and then quit the browser
   html = browser.html
   news_soup = soup(html, 'html.parser')
   # Add try/except for error handling
   try:
       slide_elem = news_soup.select_one('div.list_text')
       news_title = slide_elem.find("div", class_="content_title").get_text()
       news_p = slide_elem.find("div", class_="article_teaser_body").get_text()
   except AttributeError:
       return None, None
   return news_title, news_p

#Featured Image
def featured_image(browser):
    url1 = 'https://spaceimages-mars.com/'
    browser.visit(url1)
    html1 = browser.html
    news_soup1 = soup(html1, 'html.parser')
    try:
        slide_elem1 = news_soup1.select_one('div.floating_text_area')
        image_url_location = slide_elem1.find('a')
        image_url= image_url_location['href']
    except AttributeError:
        return None
    featured_image_url= (f'{url1}{image_url}')
    return(featured_image_url)


def mars_facts():
    #Mars Facts
    url2 = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(url2)
    tables_df= tables[0]
    tables_df=tables_df.rename(columns={0:'Description', 1:'Mars', 2:'Earth'})
    tables_df.set_index('Description')
    tables_df.to_html("Mars Facts.html")
    return(tables_df)


def mars_hemisphere(browser):
    #Mars Hemispheres
    url3= ['https://marshemispheres.com/cerberus.html', 'https://marshemispheres.com/schiaparelli.html', 'https://marshemispheres.com/syrtis.html', 'https://marshemispheres.com/valles.html']
    titles_img=[]

    for item in url3:
        browser.visit(item)
        html3 = browser.html

        news_soup3 = soup(html3, 'html.parser')
        try:
            slide_elem3 = news_soup3.select_one('img.wide-image')
            slide_elem3_url= item +'/'+ slide_elem3['src']
            slide_elem4 = news_soup3.select_one('div', class_='cover')
        except AttributeError:
            return None
        list1=[slide_elem4.h2.text, slide_elem3_url]
        titles_img.append(list1)

    hemisphere_image_url=[]
    for title, img in titles_img:
        hemisphere_dict={'Title':title, 'img_url': img}
        hemisphere_image_url.append(hemisphere_dict)

    return(hemisphere_image_url)