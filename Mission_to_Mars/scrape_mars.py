from bs4 import BeautifulSoup
import requests
from splinter import Browser
import selenium
import pandas as pd
import time

#Take the url, get a request out of it, then make some soup
url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204%3A19&blank_scope=Latest"
request = requests.get(url)
soup = BeautifulSoup(request.text, 'html.parser')

#Next to find all the image containers and assign them as a list to a variable
container_box = soup.find_all('div', class_='image_and_description_container')

#From inside those containers I can get the Title and Paragraph of the first story and assing to variables
title = container_box[0].find_all('img')[1]['alt']
para = container_box[0].find_all('a')[0].text.strip()

#################################################################################

# Create an executable path, initialize chrome driver
executable_path = {"executable_path": "chromedriver.exe"}
browser = Browser("chrome", **executable_path)

#Next to input the website and have the driver visit the website
jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(jpl_url)

#From here we need to use splinter functionality and click a couple of buttons to get to the right page
browser.click_link_by_id('full_image')
moreButton = browser.links.find_by_partial_text('more info')
moreButton.click()

#Now that we are at the right page, we copy this url and make soup from it
featured_url = browser.html
featured_image = BeautifulSoup(featured_url, "html.parser")

#Now to navigate the soup and find thte image then same it to a variable
jpl_image_url = featured_image.select_one("figure.lede a img").get("src")
full_feature_url = f"https://www.jpl.nasa.gov/{jpl_image_url}"

#Finally to closer the browser to be proper
browser.quit()


#################################################################################

# Create an executable path, initialize chrome driver
executable_path = {"executable_path": "chromedriver.exe"}
browser = Browser("chrome", **executable_path)

#Next to input the website and have the driver visit the website
mars_twit_url = "https://twitter.com/marswxreport?lang=en"
browser.visit(mars_twit_url)

time.sleep(10)

#Now that we are at the right page, we copy this url and make soup from it
mar_twit_url = browser.html
mar_twit = BeautifulSoup(mar_twit_url,"html.parser")

#Next to find the container of tweets and assign to a variable
twits = mar_twit.find_all("div", class_="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0")

#Next I need to make a conditional loop to make sure the tweet is about the weather and not something else
condition = False
i = 0
while condition == False:

    mars_weather = twits[i].span.text
    if ("InSight sol"):
        condition = True
    else:
        i = i+1

#Print just to double check
print(mars_weather)

#Close the browser
browser.quit()

#################################################################################

#First to place the url into a variable
mar_fact_url = "https://space-facts.com/mars/"

#Pandas makes it really easy to grab tables from websites
mar_fact = pd.read_html(mar_fact_url)[0]

#Now just to give the columns names and set the index
mar_fact.columns=["Description", "Value"]
mar_fact.set_index("Description", inplace=True)


#################################################################################

#Take the url, get a request out of it, then make some soup
mar_hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
request_hemi = requests.get(mar_hemi_url)
hemi_soup = BeautifulSoup(request_hemi.text, 'html.parser')

#Now I need to make variables of the two containers I want
hemi_names = hemi_soup.find_all('h3')
hemi_links = hemi_soup.find_all('a',class_='itemLink product-item')

#Now we need and empty list to store the dictionaries
hemisphere_image_urls = []

#A variable for the base url
mini_url = "https://astrogeology.usgs.gov"

#Here I am making a for loop that goes through both my links and gets the information I need from it.
for name,links in zip(hemi_names, hemi_links):
    hemi_name = name.text.replace(" Enhanced","")
    full_url = mini_url + links['href']
    full_image_request = requests.get(full_url)
    full_image_soup = BeautifulSoup(full_image_request.text, 'html.parser')
    full_image_link = full_image_soup.find('img', class_="wide-image")
    full_image_total_url = mini_url + full_image_link['src']
    hemisphere_image_urls.append({'title':hemi_name,"img_url":full_image_total_url})
    time.sleep(1)
