
# Import Splinter and BeautifulSoup
from tkinter import BROWSE
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt
import selenium

def scrape_all():

    # initiate headless driver
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    news_title, news_paragraph = mars_news(browser)
    hemisphere_image_urls = mars_hemi(browser)

    # run scraping functions and store results in dictionary
    data = {
            "news_title": news_title,
            "news_paragraph": news_paragraph,
            "featured_image": featured_image(browser),
            "facts": mars_facts(),
            "hemispheres": hemisphere_image_urls,
            "last_modified": dt.datetime.now()   
    } 

    browser.quit()

    return data

def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    html = browser.html
    news_soup = soup(html, 'html.parser')

    # error handling
    try:

        slide_elem = news_soup.select_one('div.list_text')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:

        return None, None
        
    return news_title, news_p

def featured_image(browser):

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:

        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:

        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url

def mars_facts():
    
    try:

        # use 'read_html" to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    
    except BaseException:

        return None

    # assign column names and set index of DataFrame
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
        
    # convert DataFrame into HTML ready code
    return df.to_html()

def mars_hemi(browser):

    # visit the mars hemispheres site
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # Parse the resulting html with soup
    html = browser.html
    hemi_soup = soup(html, 'html.parser')
    
    hemisphere_image_urls = []

    # retrieve the image urls and titles for each hemisphere.
    for i in range (4):
        
        hemi_info = {}

        browser.is_element_present_by_css('a.product-item img', wait_time=2)
        browser.find_by_tag('h3')[i].click()

        full_size = browser.find_by_text('Sample')
        url = full_size['href']
        
        title = browser.find_by_tag('h2').text
        
        hemi_info['image_url'] = url
        hemi_info['title'] = title
        
        hemisphere_image_urls.append(hemi_info)
        
        browser.back()

    return hemisphere_image_urls
   
if __name__ == "__main__":
    
    # If running as script, print scraped data
    print(scrape_all())

