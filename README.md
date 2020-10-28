# PyAnimeList
Retrieve your favourite anime or search for recommendations through filtering and sorting.

## Aim
The aim of this project is to store and retrieve data from MyAnimeList: https://myanimelist.net/

Users can retrieve data of their favourite Anime/Donghua from the most updated MyAnimeList site in Python.

A sorting and querying method is also provided that allows users to retrieve Anime/Donghua based on their preferences.

## Setting Up
This model is written in both Jupyter Notebook version 4.4.0 and Python version 3.7.1. You may use any integrated development environment (IDE)
to run the program using a Python interpreter but Visual Studio Code or Jupyter Notebook is highly recommended thanks to their Python Interactive window.

The notebook document can be found at PyAnimeList.ipynb while the Python file can be found at PyAnimeList.py. Either file should run the program for sorting
and querying. 

The data is taken using the Jikan (Kanji: 時間) API, an open source PHP and REST API that parses website data from MyAnimeList. There is a Python wrapper for Jikan
using JikanPy.

## Visuals
![visuals](https://imgur.com/GwsGDVS.jpg)
Example of anime filtering using a MyAnimeList average score of higher than 7, with the Slice of Life genre between 2010 and 2020, sorted by the number of members (popularity).

## Future Work
Moving forward, machine learning can be implemented in PyAnimeList to recommend anime based on previous user input. This can be done by recommending
users anime based on genre and score that were input by the user. Natural Language Processing should provide the necessary models for anime recommendation.
