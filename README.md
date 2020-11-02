# PyAnimeList
Retrieve your favourite anime or search for recommendations through filtering and sorting or the PyAnimeList anime recommender system.

## Aim
The aim of this project is to store and retrieve data from MyAnimeList: https://myanimelist.net/.

Users can retrieve data of their favourite Anime/Donghua from the most updated MyAnimeList site in Python.

The program is divided into phases (WIP):
* Phase 1 (26 Oct 2020): A sorting and querying method is provided that allows users to retrieve Anime/Donghua based on their preferences. Users can select attributes such as title, genre or score to retrieve anime data and sort based on these attributes.

* Phase 2 (2 Nov 2020): An NLP-based recommender system using cosine similarity allows users to input the title of an anime to retrieve similar anime. This system allows recommending users similar anime based on genre, synopsis and anime producer.

## Setting Up
This model is written in both Jupyter Notebook version 4.4.0 and Python version 3.7.1. You may use any integrated development environment (IDE)
to run the program using a Python interpreter but Visual Studio Code or Jupyter Notebook is highly recommended thanks to their Python Interactive window.

The notebook document can be found at PyAnimeList.ipynb while the Python file can be found at PyAnimeList.py. Either file should run the program for sorting
and querying. 

The data is taken using the Jikan (Kanji: 時間) API, an open source PHP and REST API that parses website data from MyAnimeList. There is a Python wrapper for Jikan
using JikanPy.

## Visuals
![visuals](https://imgur.com/GwsGDVS.jpg)

Phase 1: Example of anime filtering using a MyAnimeList average score of higher than 7, with the Slice of Life genre between 2010 and 2020, sorted by the number of members (popularity).


![visuals](https://imgur.com/XSh2V5L.jpg)

Phase 2: Example of the anime recommender system, recommending anime similar to New Game!

## Future Work
Moving beyond Phase 2, PyAnimeList can recommend users anime (Phase 2) based on genre and score that were input by the user through the search function (Phase 1). By gathering information of several anime searches by the user, the program could provide personalised recommendations without the need of manual user input. The personalised recommendations could also contain data besides the anime's title, such as score, genre and synopsis. Case sensitivity and syntax could also be further relaxed, allowing users to search anime without needing an exact match. 
