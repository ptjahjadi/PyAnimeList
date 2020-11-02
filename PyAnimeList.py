#!/usr/bin/env python
# coding: utf-8

# PyAnimeList by Patrick Tjahjadi
# 
# Program to retrieve Anime/Donghua data from MyAnimeList, including score, year, genre, etc.
# 
# Allows users to filter Anime/Donghua based on these attributes with a sorting feature.
# 
# Search for your favourite Anime/Donghua or simply look for recommendation with the filtering and sorting feature!

# In[3]:


# Imported Libraries
from jikanpy import Jikan
import pandas as pd
import time
from IPython.display import clear_output
import dill
from rake_nltk import Rake
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer


# In[4]:


# We can load this later instead of retrieving data again
# dill.load_session('my_anime_list.db')


# In[2]:


# Function to clean words from punctuation and remove capital case to standardise text tokens
def clean_text(word):
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_123456789~'''
    no_punct = ""
    for char in word:
        if char not in punctuations:
            no_punct = no_punct + char
    return no_punct.lower()


# In[3]:


# Set up data for anime from 2000 to 2020 for retrieval using the Jikan API

jikan = Jikan()

years = [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010,
         2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]
seasons = ['winter', 'spring', 'summer', 'fall']

myanimelist = []


# In[4]:


# Retrieve anime data through Jikan
# Time delay of 7 seconds per year for API rate limiting
for year in years:
    for season in seasons:
        myanimelist.append(jikan.season(year = year, season = season))
    time.sleep(7)


# PHASE 1: Store and retrieve anime data in dataframes for search and sort

# In[6]:


# Collect all necessary attributes: Title, Score, Members, Genre, Producers, Year, Season and Synopsis
animedata = []
for animeseason in myanimelist:
    for show in animeseason['anime']:
        animedata.append([show['title'], show['score'], show['members'], ', '.join(genre['name'] for genre in show['genres']), 
                        ', '.join(producer['name'] for producer in show['producers']), animeseason["season_year"],
                        animeseason["season_name"], show['synopsis']])
        


# In[7]:


# Create a dataframe to store Anime data and remove duplicate entries
anime_df = pd.DataFrame(animedata, columns = ["Title", "Score", "Members", "Genre", "Producers", "Year", "Season", "Synopsis",])
anime_df.drop_duplicates(subset="Title", keep = 'first', inplace = True)
anime_df.index.name = "Anime ID"


# In[3]:


# Function to retrieve anime based on filtering and sorting input
def get_my_anime(output_anime_df):
    list_of_queries = []
    list_of_sort = ["None"]
    while (1):
        print("Your queries: \n"+", ".join(list_of_queries))
        method = input("Search anime based on (Title, Score, Members, Genre, Year, Season or Synopsis)? Otherwise, input 0.\n")
        if (method == "0"):
            break
        elif (method.lower() in ["title", "score", "members", "genre", "year", "season", "synopsis"]):
            output_anime_df = query_my_anime(output_anime_df, method, list_of_queries)
    output_anime_df = sort_my_anime(output_anime_df, list_of_queries, list_of_sort)
    clear_output(wait=True)
    print("Your queries: \n"+", ".join(list_of_queries))
    print("Your sorting method: \n"+list_of_sort[0])
    return output_anime_df

# Function to filter anime based on attributes
def query_my_anime(interim_df, method, list_of_queries):
    if (method.lower() in ["title", "genre", "producers", "season", "synopsis"]):
        query_content = input("Search by anime "+method.capitalize()+":\n")
        interim_df = interim_df.query('{}.str.contains("{}")'.format(method.capitalize(), query_content), engine = 'python')
        list_of_queries.append("{}: {}".format(method.capitalize(), query_content))
    elif (method.lower() in ["score", "members", "year"]):
        operator = input("Find anime "+method.capitalize()+" less than, equal to, greater than, or range (L = Less, E = Equal, G = Greater, R = Range)?\n")
        if (operator.lower() in ["g", "greater", "greater than"]):
            value = input("Greater than which "+method.capitalize()+ "?\n")
            interim_df = interim_df.query('{} > {}'.format(method.capitalize(), value))
            list_of_queries.append("{} > {}".format(method.capitalize(), value))
        elif (operator.lower() in ["e", "equal", "equal to"]):
            value = input("Equal to which "+method.capitalize()+ "?\n")
            interim_df = interim_df.query('{} == {}'.format(method.capitalize(), value))
            list_of_queries.append("{} = {}".format(method.capitalize(), value))
        elif (operator.lower() in ["l", "less", "less than"]):
            value = input("Less than which "+method.capitalize()+ "?\n")
            interim_df = interim_df.query('{} < {}'.format(method.capitalize(), value))
            list_of_queries.append("{} < {}".format(method.capitalize(), value))
        elif (operator.lower() in ["r", "range"]):
            value_low = input("Between which values inclusive? Set lower limit:\n")
            value_high = input("Between which values inclusive? Set upper limit:\n")
            interim_df = interim_df.query('{} > {} and {} < {}'.format(method.capitalize(), value_low, method.capitalize(), value_high))
            list_of_queries.append("{} <= {} <= {}".format(value_low, method.capitalize(), value_high))
    clear_output(wait=True)        
    return interim_df

# Functions to sort the order of anime to be output
def sort_my_anime(interim_df, list_of_queries, list_of_sort):
    clear_output(wait = True)
    print("Your queries: \n"+", ".join(list_of_queries))
    while (1):
        sort_attribute = input("Any sorting method (Title, Score, Members, Genre, Year, Season or Synopsis)? Otherwise, input 0.\n")
        if (sort_attribute.lower() in ["title", "score", "members", "genre", "year", "season", "synopsis"]):
            while (1):
                sort_method = input("Ascending or Descending (A = Ascending, D = Descending)?")
                if (sort_method.lower() in ["a", "ascending"]):
                    interim_df = interim_df.sort_values(sort_attribute.capitalize(), ascending = True)
                    list_of_sort[0] = sort_attribute.capitalize()+": Ascending"
                    return interim_df
                elif (sort_method.lower() in ["d", "descending"]):
                    interim_df = interim_df.sort_values(sort_attribute.capitalize(), ascending = False)
                    list_of_sort[0] = sort_attribute.capitalize()+": Descending"
                    return interim_df
        elif (sort_attribute == "0"):
            return interim_df


# In[4]:


# Query and search for anime here!
query_df = get_my_anime(anime_df)
query_df


# PHASE 2: Use natural language processing to determine anime similarity for recommendation

# In[10]:


# Initializing a keywords column for natural language processing
anime_df['Keywords'] = ""

count = 0
# Iterate through each anime and get their keywords
for index, row in anime_df.iterrows():
    # Input double weighting on genre so recommendations are more genre-based
    keyword_order = [row['Synopsis'], row['Genre'], row['Genre'], row['Producers']]
    keywords = " ".join(keyword_order)

    # Use rake to discard English stopwords
    r = Rake()

    # Extracting the keywords by passing the text
    r.extract_keywords_from_text(keywords)

    # Get the dictionary with keywords as keys and scores as values
    # Score = Degree(word) / Frequency(word)
    key_words_dict_scores = r.get_word_degrees()
    
    # Remove punctuations from all keywords
    wordlist = list(key_words_dict_scores.keys())
    for index in range(0, len(wordlist)):
        wordlist[index] = clean_text(wordlist[index])
    
    # Assign the key words to the keywords column
    anime_df['Keywords'].iloc[count] = " ".join(wordlist)
    count+= 1


# In[11]:


# Calculate frequency of keywords and generate the count matrix 
count = CountVectorizer()
count_matrix = count.fit_transform(anime_df['Keywords'])

# Generate the cosine similarity matrix
cosine_sim = cosine_similarity(count_matrix, count_matrix)


# In[12]:


# Store the Python data into byte streams for faster future processing
dill.dump_session('my_anime_list.db')


# In[5]:


# Recommend anime based on cosine similarity

anime_titles = list(anime_df['Title'])

def anime_recommendations(cosine_sim = cosine_sim):
    anime_title = input("Input an anime title for recommendation:\n")
    recommended_anime = []
    
    idx = anime_titles.index(anime_title)

    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)


    top_10_indexes = list(score_series.iloc[1:11].index)
    for index in top_10_indexes:
        recommended_anime.append(anime_df.Title.iloc[index])
    clear_output(wait=True)
    print("Anime similar to "+anime_title+" are:")
    for anime in recommended_anime:
        print(anime)


# In[7]:


# Run the recommender here
anime_recommendations()


# In[ ]:




