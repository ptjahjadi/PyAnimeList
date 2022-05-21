# PyAnimeList
Retrieve data about animimation shows through filtering and sorting or search for recommendation using a cosine-similarity based recommender system. Data includes shows from Winter 2020 - Fall 2022.

## Aim
The aim of this project is to store and retrieve data from MyAnimeList: https://myanimelist.net/.

Users can retrieve data of their favourite Anime/Donghua from the most updated MyAnimeList site in Python.

The program is divided into phases (WIP):
* Phase 1 (26 Oct 2020): A sorting and querying method is provided that allows users to retrieve Anime/Donghua based on their preferences. Users can select attributes such as title, genre or score to retrieve anime data and sort based on these attributes.

* Phase 2 (2 Nov 2020): An NLP-based recommender system using cosine similarity allows users to input the title of an anime to retrieve similar anime. This system allows recommending users similar anime based on genre, synopsis and anime producer.

* Phase 2.1 (7 Nov 2020): Updates to the querying and recommender system for ease of usage. This includes an additional feature for querying that accepts number of results as user input. The recommender system is now case-insensitive and is able to return the closest anime search to the user input.

* Phase 3 (22 Nov 2020): The NLP-based recommender system has been developed to also account for previous user queries in Phase 1. The top queried anime will be used as recommendations, allowing for a more personalised recommendation. The more times the user queries, the more varied the system in recommending anime.

* Phase 3.1 (10 July 2021): The anime querying method is now able to accept filters without case sensitivity. The show title is also taken into account in keywords for recommendation, leading to a more accurate prediction of similar shows.

## Setting Up
This model is written in both Jupyter Notebook version 4.4.0 and Python version 3.7.1. You may use any integrated development environment (IDE)
to run the program using a Python interpreter but Visual Studio Code or Jupyter Notebook is highly recommended thanks to their Python Interactive window.

The notebook document can be found at PyAnimeList.ipynb while the Python file can be found at PyAnimeList.py. Either file should run the program for sorting
and querying. 

The data is taken using the Jikan (Kanji: 時間) API, an open source PHP and REST API that parses website data from MyAnimeList. There is a Python wrapper for Jikan
using JikanPy.

## Visuals
![visuals](https://imgur.com/PMzOzlO.jpg)

Phase 1: Example of anime filtering using a MyAnimeList average score between 7 and 9, with the Slice of Life genre and made after 2010, sorted by the number of members (popularity) with 5 results.


![visuals](https://imgur.com/XSh2V5L.jpg)

Phase 2: Example of the anime recommender system, recommending anime similar to New Game!


![visuals](https://imgur.com/ZXw0zdU.jpg)

Phase 3: Example of the anime recommender system, after the user queries for Toradora!, Mahou Shoujo Madoka★Magica, and Ojamajo Doremi Sharp.

## Future Work
Moving beyond Phase 3.1, the query in Phase 1 can be further improved by considering minor typographical errors. For instance, being able to detect the user's genre input "slice of lief" as "Slice of Life".
