
# In[3]:

from jikanpy import Jikan
import pandas as pd
import time
from IPython.display import clear_output
import dill

# In[4]:

dill.load_session('my_anime_list.db')


# In[6]:

animedata = []
for animeseason in myanimelist:
    for show in animeseason['anime']:
        animedata.append([show['title'], show['score'], show['members'], ', '.join(genre['name'] for genre in show['genres']), 
                        ', '.join(producer['name'] for producer in show['producers']), animeseason["season_year"],
                        animeseason["season_name"], show['synopsis']])
        


# In[7]:


anime_df = pd.DataFrame(animedata, columns = ["Title", "Score", "Members", "Genre", "Producers", "Year", "Season", "Synopsis",])
anime_df.index.name = "Anime ID"


# In[8]:


anime_df.drop_duplicates(subset="Title", keep = 'first', inplace = True)

# In[10]:


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


# In[12]:


query_df = get_my_anime(anime_df)
query_df

