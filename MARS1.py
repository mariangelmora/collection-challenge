#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup


# In[ ]:





# In[2]:


browser = Browser('chrome')


# In[3]:


# Visit the Mars news site
url = 'https://static.bc-edx.com/data/web/mars_news/index.html'
browser.visit(url)


# In[4]:


# Extract HTML content from the browser
html = browser.html

# Create a BeautifulSoup object
mars_soup = soup(html, 'html.parser')


# In[5]:


# Extract all the text elements
text_elements = mars_soup.find_all(text=True)



# In[6]:


# Extract all the text elements
all_text = mars_soup.get_text()


# In[9]:


article_containers = mars_soup.find_all('div', class_='list_text')

# Create an empty list to store the dictionaries
news_articles = []

# Extract the title and preview text
for container in article_containers:
    title = container.find('div', class_='content_title').text.strip()
    preview = container.find('div', class_='article_teaser_body').text.strip()
    
    # Store the title and preview text in a dictionary
    article_dict = {'title': title, 'preview': preview}
    
    # Add the dictionary to the list
    news_articles.append(article_dict)
    print(news_articles)


# In[22]:


browser.quit()


# In[ ]:




