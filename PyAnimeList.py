#!/usr/bin/env python
# coding: utf-8

# PyAnimeList by Patrick Tjahjadi
# 
# Program to retrieve Anime/Donghua data from MyAnimeList, including score, year, genre, etc.
# 
# Allows users to filter Anime/Donghua based on these attributes with a sorting feature.
# 
# Program also includes a cosine-similarity based recommender system to recommend shows you like.

# In[1]:


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
import difflib


# In[2]:


# Function to ask for an anime title and recommend anime based on cosine similarity
def anime_recommendations(cosine_sim, number_anime):
    anime_titles = list(anime_df['Title'])
    # Create another list to remove case sensitivity in searching anime
    anime_titles_lower = [title.lower() for title in anime_titles]      
    anime_title = input("Input an anime title for recommendation:\n")
    
    # Recommend an anime if a similar match is found
    try:
        anime_title = difflib.get_close_matches(anime_title.lower(), anime_titles_lower, n = 1, cutoff = 0.5)[0]
        
        # Find the position of the anime title in the list
        idx = anime_titles_lower.index(anime_title)
        
        # Retrieve the top 10 most similar anime based on cosine similarity
        score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)
        clear_output(wait=True)
        print("Anime similar to "+anime_titles[idx]+" are:")
        top_10_indexes = list(score_series.iloc[1:(number_anime + 1)].index)
        for index in top_10_indexes:
            print(anime_df.Title.iloc[index])
            
    except IndexError:
        print("No results found.")


# In[3]:


# Function to recommend anime based on query results in Phase 1
def anime_recommendations_from_query(query_recommendation_list, cosine_sim, number_anime):
    anime_titles = list(anime_df['Title'])
    num_output = round(number_anime / len(query_recommendation_list)) + 1
    top_anime = []
    for recommended_title in query_recommendation_list:
        anime_title = difflib.get_close_matches(recommended_title, anime_titles, n = 1, cutoff = 0.5)[0]
        idx = anime_titles.index(anime_title)
        score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)
        testlist = list(score_series.iloc[1:num_output].index)
        top_anime.append(testlist)

    print("Based on your recent queries, here are some recommended anime for you:")
    for each_recommended_anime in top_anime:
        for index in each_recommended_anime:
            print(anime_df.Title.iloc[index])


# In[4]:


# Function to clean words from punctuation and remove capital case to standardise text tokens
def clean_text(word):
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_0123456789~'''
    no_punct = ""
    for char in word:
        if char not in punctuations:
            no_punct = no_punct + char
    return no_punct.lower()


# In[2]:


# We can load this later instead of retrieving data again
dill.load_session('my_anime_list.db')


# In[7]:


"""
Skip running this block if the session "my_anime_list.db" has been loaded
"""

# Set up data for anime from 2000 to 2020 for retrieval using the Jikan API

jikan = Jikan()

years = [year for year in range (2000, 2023)]
seasons = ['winter', 'spring', 'summer', 'fall']

myanimelist = []


# In[12]:


"""
Skip running this block if the session "my_anime_list.db" has been loaded
"""

# Retrieve anime data through Jikan
for year in years:
    for season in seasons:
        myanimelist.append(jikan.season(year = year, season = season))
        


# PHASE 1: Store and retrieve anime data in dataframes for search and sort

# In[47]:


# Collect all necessary attributes: Title, Score, Members, Genre, Producers, Year, Season and Synopsis
animedata = []
for animeseason in myanimelist:
    for show in animeseason['anime']:
        animedata.append([show['title'], show['score'], show['members'], ', '.join(genre['name'] for genre in show['genres']), 
                        ', '.join(producer['name'] for producer in show['producers']), animeseason["season_year"],
                        animeseason["season_name"], show['synopsis']])
        


# In[48]:


# Create a dataframe to store Anime data and remove duplicate entries
anime_df = pd.DataFrame(animedata, columns = ["Title", "Score", "Members", "Genre", "Producers", "Year", "Season", "Synopsis"])
anime_df.drop_duplicates(subset= "Title", keep = 'first', inplace = True)
anime_df.index.name = "ID"


# In[49]:


query_recommendation_list = []

# Function to retrieve anime based on filtering and sorting input
def get_my_anime(output_anime_df):
    list_of_queries = []
    list_of_sort = ["None"]
    query_loop = 0
    while (1):
        if (query_loop == 1):
            print("Your queries: \n"+", ".join(list_of_queries))
        method = input("Search anime based on (Title, Score, Members, Producers, Genre, Year, Season or Synopsis)? Otherwise, input 0.\n")
        if (method == "0"):
            break
        elif (method.lower() in ["title", "score", "members", "producers", "genre", "year", "season", "synopsis"]):
            output_anime_df = query_my_anime(output_anime_df, method, list_of_queries)
        query_loop = 1
    
    # Prefill the list of queries if the user searches without any query
    if not list_of_queries:
        list_of_queries = ["None"]
    output_anime_df = sort_my_anime(output_anime_df, list_of_queries, list_of_sort)
    clear_output(wait=True)
    
    # Print queries and sorting method, and ask for how many results to be output
    print("Your queries: \n"+", ".join(list_of_queries))
    print("\nYour sorting method: \n"+list_of_sort[0])
    limit = int(limit_my_anime())
    
    # Print queries, sorting method and the number of output results
    clear_output(wait=True)
    print("Your queries: \n"+", ".join(list_of_queries))
    print("\nYour sorting method: \n"+list_of_sort[0])
    print("\nYour search yields", output_anime_df.head(limit).shape[0], "results")
    # If the keywords column is present, remove it for querying
    try:
        output_anime_df.drop(columns = ['Keywords'], inplace = True)
    except:
        pass
    return output_anime_df.head(limit)

# Function to filter anime based on attributes
def query_my_anime(interim_df, method, list_of_queries):
    # For string-based variables, ask the user for string input and the algorithm will return anime
    # that contains the string input
    if (method.lower() in ["title", "genre", "producers", "season", "synopsis"]):
        query_content = input("Search by anime "+method.capitalize()+":\n")
        interim_df = interim_df.query('{}.str.contains("{}", case = False)'.format(method.capitalize(), query_content),
                                      engine = 'python')
        list_of_queries.append("{}: {}".format(method.capitalize(), query_content))
    
    # For number-based variables, ask the user if they would like to query less than, equal to or greater than
    # a particular number or if they would like to specify a numerical range
    elif (method.lower() in ["score", "members", "year"]):
        operator = input("Find anime "+method.capitalize()+
                         " less than, equal to, greater than, or range (L = Less, E = Equal, G = Greater, R = Range)?\n")
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
            interim_df = interim_df.query('{} > {} and {} < {}'.format
                             (method.capitalize(), value_low, method.capitalize(), value_high))
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
                sort_method = input("Ascending or Descending (A = Ascending, D = Descending)?\n")
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
        
def limit_my_anime():
    limit = input("How many results would you like?")
    return limit


# In[50]:


# Query and search for anime here!
query_df = get_my_anime(anime_df)

# Add the top result of the query to the recommendation list, if it exists
try:
    if query_df["Title"].iloc[0] not in query_recommendation_list:
        query_recommendation_list.append(query_df["Title"].iloc[0])
except IndexError:
    pass
query_df


# PHASE 2: Use natural language processing to determine anime similarity for recommendation

# In[51]:


"""
Skip running this block if the session "my_anime_list.db" has been loaded
"""

# Initializing a keywords column for natural language processing
anime_df['Keywords'] = ""

count = 0
# Iterate through each anime and get their keywords
for index, row in anime_df.iterrows():
    # Input relevant keywords such as synopsis, genre, title and producer
    keyword_order = [row['Synopsis'], row['Genre'], row['Title'], row['Producers']]
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
    clean_wordlist = []
    for index in range(0, len(wordlist)):
        wordlist[index] = clean_text(wordlist[index])
        if wordlist[index] != "":
            clean_wordlist.append(wordlist[index])

    # Assign the key words to the keywords column
    anime_df['Keywords'].iloc[count] = " ".join(clean_wordlist)
    count+= 1


# In[52]:


"""
Skip running this block if the session "my_anime_list.db" has been loaded
"""

# Calculate frequency of keywords and generate the count matrix 
count = CountVectorizer()
count_matrix = count.fit_transform(anime_df['Keywords'])

# Generate the cosine similarity matrix
cosine_sim = cosine_similarity(count_matrix, count_matrix)


# In[53]:


# Store the Python data into byte streams for faster future processing
dill.dump_session('my_anime_list.db')


# In[56]:


# Run the recommender here, and set the number of anime to be recommended in the second parameter
anime_recommendations(cosine_sim, 10)


# PHASE 3: Provide personalised anime recommendations to users through the results of their queries

# In[57]:


# Run the recommender here, and set the number of anime to be recommended in the third parameter
anime_recommendations_from_query(query_recommendation_list, cosine_sim, 20)


# In[64]:


anime_df.to_csv('anime_data.csv', index=True)


# In[ ]:




