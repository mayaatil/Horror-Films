from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector
import requests
from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS
import matplotlib.pyplot as plt
import sqlite3

# helps render image
from PIL import Image

# path functions to help access the image
from os import path, getcwd

# render image correctly for our function
import numpy as np

# import nltk
# nltk.download('all')

# import scipy.sparse.linalg as sp
# id = np.eye(13)
# vals, vecs = sp.eigsh(id, k=6)
# vals

# natural language processing toolkit to help process our data
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# create function so that it is more generalized - can be used for other scenarios
def get_soup(html):
    """ get data for web page"""
    resp = requests.get(film_list)
    # if charcleacterset is in the header of content type then we'll convert to lower case or else we will not include it
    http_encoding = resp.encoding if 'charset' in resp.headers.get('content-type', '').lower() else None
    html_encoding = EncodingDetector.find_declared_encoding(resp.content, is_html=True)
    # encoding variable to include if it is http or html
    encoding = html_encoding or http_encoding
    # we'll get content of response from the request we made (see line 23) and we'll use this type of encoding to return soup object, which includes all html content for the website
    soup = BeautifulSoup(resp.content, features="html.parser")
    return soup

def get_links(soup):
    """ Get links from a web page """
    http_link_list = [] 
    for link in soup.find_all('a', href=True):
        if link['href']!= '/': 
            http_link_list.append(link['href'].strip("'"))
    return http_link_list 

def get_ps(soup):
    """ get <h1> tags from web page"""
    http_link_list = [] 
    for link in soup.find_all('h3'):
        http_link_list.append(link.get_text())
    return http_link_list 

def get_text(text_array):
    """ get text from an array"""
    text = " ".join(text_array)
    return text

def get_film_text(film_list):
    """get text from all film in list"""
    text_return = []
    for i in film_list:
        print(i)
        soup = get_soup(i)
        text_array = get_ps(soup)
        full_text = get_text(text_array)
        text_return.append(full_text)
    return text_return    

def punctuation_stop(text):
    """remove punctuation and stop words"""
    filtered = []
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)
    for w in word_tokens:
        if w not in stop_words and w.isalpha():
            filtered.append(w.lower())
    return filtered


#webpage
film_list = "https://www.timeout.com/film/best-horror-films"

#gets word soup from website 
soupout = get_soup(film_list)
soupout

#gets links from website     
h_links = get_links(soupout)

html_links = h_links[0:30]

#return list of all episode text 
text_return_list = get_film_text(html_links)
all_text = get_text(text_return_list)

#removed punctuation and stop words 
filteredlst = punctuation_stop(all_text)

# #list of unwanted words 
unwanted = ['noble']

#remove unwanted words 
text = " ".join([ele for ele in filteredlst if ele not in unwanted])

#get the working directory 
d = getcwd()

#numpy image file of mask image 
mask = np.array(Image.open("halloween-logo.jpg"))

#create the word cloud object 
wc= WordCloud(background_color="black", max_words=2000, max_font_size=50, random_state=1, mask=mask, stopwords=STOPWORDS)
wc.generate(text)

image_colors = ImageColorGenerator(mask)

plt.figure(figsize=[10,10])
plt.imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")
plt.axis('off')
plt.show()