"""
work with database of books
"""
import json
import re
import csv
from tqdm import tqdm
import pandas as pd

pd.set_option('display.max_colwidth', 300)

print('reading books info')

# read info about books from booksummaries.txt and convert it to normal form
data = []

with open("./database/books/booksummaries.txt", 'r') as file:
    reader = csv.reader(file, dialect='excel-tab')
    for row in tqdm(reader):
        data.append(row)

book_name = []
book_author = []
publication_date = []
summary = []
genres = []


for i in tqdm(data):
    book_name.append(i[2])
    book_author.append(i[3])
    publication_date.append(i[4])
    genres.append(i[5])
    summary.append(i[6])

books = pd.DataFrame({'book_name': book_name,
                      'author': book_author,
                      'publication': publication_date,
                      'genres': genres,
                      'summary': summary})
del book_name
del book_author
del publication_date
del summary
del genres

books.drop(books[books['genres'] == ''].index, inplace=True)
genres = []
for i in books['genres']:
    genres.append(list(json.loads(i).values()))
books['genres'] = genres
books['genres'] = books['genres'].apply(set)
del genres


def clean_summary(text: str) -> str:
    """
    function convert string from database into normal form
    """
    text = re.sub("\'", "", text)
    text = re.sub("[^a-zA-Z]", " ", text)
    text = ' '.join(text.split())
    text = text.lower()
    return text


books['summary'] = books['summary'].apply(clean_summary)

# read extra info about books from books.csv Convert it to normal form and
# add it to database books

extra_data = pd.read_csv('./database/books/books.csv')
extra_data = extra_data.loc[:, ~extra_data.columns.str.contains('^Unnamed')]
extra_data = extra_data.drop(columns={'publisher', 'text_reviews_count'})


def clean_title(title: str):
    """
    function convert title string from database into normal form
    """
    try:
        index = title.index(' (')
        title = title[:index]
    except ValueError:
        pass
    return title


extra_data['title'] = extra_data['title'].apply(clean_title)
# extra_data['average_rating'] = extra_data['average_rating'].apply(float)

names = set(extra_data['title'])
books = books[~books['book_name'].isin(names)]
names = set(books['book_name'])
extra_data = extra_data[~extra_data['title'].isin(names)]

books.reset_index(inplace=True, drop=True)
extra_data.reset_index(inplace=True, drop=True)

dct_names = {}
for i in range(len(extra_data)):
    dct_names[str(extra_data['title'][i])] = i
books['isbn'] = None
books['rating'] = None
books['num_pages'] = None
books['publication_date'] = None
books_len = len(books)
for i in tqdm(range(books_len)):
    try:
        ind = dct_names[extra_data['title'][i]]
        books['isbn'][i] = extra_data['isbn'][ind]
        books['num_pages'][i] = extra_data['num_pages'][ind]
        books['publication_date'][i] = extra_data['publication_date'][ind]
        books['rating'][i] = extra_data['average_rating'][ind]
    except KeyError:
        books = books.drop(i)
del extra_data

# add column of marks of each book
books['mark'] = books['rating']

# give correct data types
books['rating'] = pd.to_numeric(books['rating'])
books['mark'] = pd.to_numeric(books['mark'])
books['mark'] = books['mark'].apply(lambda x: x * 2)

books = books.rename(columns={'book_name': 'title', 'genres': 'genre',
                              'summary': 'desc'})
books = books.drop_duplicates(subset=['title'], keep='last')
books.reset_index(inplace=True, drop=True)

# write books dataset into file
# books.to_csv('./book_info.csv')

print('complete reading books info\n')
