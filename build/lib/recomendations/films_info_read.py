"""
work with database of films
"""
import ast
from tqdm import tqdm
import pandas as pd

pd.set_option('display.max_colwidth', 120)
pd.options.display.max_rows = 9

print('reading films info')

RATING = 3
VOTES = 50
print('.', end='')
# read and format films dataset from file
films = pd.read_csv("database/films/movies_metadata.csv")
films = films[films['vote_count'] > VOTES]
films = films[films['vote_average'] > RATING]
films['overview'] = films['overview'].apply(lambda x: str(x).lower())


def convert_data(genres: str) -> set:
    """
    function covert string with info to set with needed values
    clean_genres("[{'id':16, 'name':'Animation'}, {'id':35, 'name':'Comedy'},\
{'id':10751, 'name':'Family'}]")
    {'Animation', 'Comedy', 'Family'}
    """
    genres = genres[1:-1].split(', ')
    genres = [genres[2 * ind] + ', ' + genres[2 * ind + 1]
              for ind in range(len(genres) // 2)]
    genres = list(map(ast.literal_eval, genres))
    genres = {genre['name'] for genre in genres}
    return genres


films['genres'] = films['genres'].apply(convert_data)
films['prod_countries'] = films['prod_countries'].apply(convert_data)
films.index = list(films['imdb_id'])

print('.', end='')

# read and format key_words from file
key_words = pd.read_csv("database/films/keywords.csv")
key_words['keywords'] = key_words['keywords'].apply(convert_data)
key_words = key_words.drop_duplicates(subset=['id'], keep='last')

# read and format links from file
links = pd.read_csv("database/films/links.csv")
func = lambda x: 'tt' + str(int(x) + 10000000)[1:]
links['imdbId'] = links['imdbId'].apply(func)
names = set(films['imdb_id'])
links = links[links['imdbId'].isin(names)]

# combine links and key_words datasets
names = set(key_words['id'])
links = links[links['movieId'].isin(names)]
names = set(links['movieId'])
key_words = key_words[key_words['id'].isin(names)]

key_words.index = list(links['imdbId'])
del links
names = set(key_words.index)
films = films[films['imdb_id'].isin(names)]

# add key_words to main dataset films
films['keywords'] = key_words['keywords']

print('.', end='\n')

films = films.rename(columns={'vote_average': 'rating', 'genres': 'genre',
                              'overview': 'desc'})

# write films dataset into file
# films.to_csv('./films_info.csv')
print('complete reading films info')
print('----------------------------------------------------------------------')
