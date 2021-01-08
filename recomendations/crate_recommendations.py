"""
this module work with created databases in modules books_info_read1.py
develop function give_rec_book_by_film

"""

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from tqdm import tqdm
from books_info_read import books as books_df
from films_info_read import films as films_df


def give_rec_book_by_film(film_imdb_id: str, num_rec=3, books=books_df,
                          films=films_df, genres=None) -> pd.DataFrame:
    """
    function return DataFrame with top of recomendation for user
    """
    def recommend_by_desc(title: str, books=books_df,
                          films=films_df) -> pd.Series:\

        book_data = books.copy()

        # Converting the book description into vectors and used bigram
        tfvectorise = TfidfVectorizer(analyzer='word', ngram_range=(1, 2),
                                      min_df=1, stop_words='english')
        book_dsc = book_data['desc'].append(films[films['title'] ==
                                                  title]['desc'],
                                            ignore_index=True)
        tfv_matrix_books = tfvectorise.fit_transform(book_dsc)

        # Calculating the similarity measures based on Cosine Similarity
        simil_matrix = cosine_similarity(tfv_matrix_books, tfv_matrix_books)

        # Get the pairwsie similarity scores
        marks_lst = simil_matrix[-1][:-1]
        marks_lst = [x * 1000 for x in marks_lst]

        rec = pd.Series(marks_lst, index=list(book_data['title']))
        return rec
    # preparing data
    books_data = books.copy()
    if genres is None:
        genres = films['genre'][film_imdb_id]

    # Matching the genre with the dataset and reset the index
    for index in tqdm(books_data.index):
        for genre in genres:
            if genre in books_data['genre'][index]:
                break
        else:
            books_data = books_data.drop([index])
    books_data.reset_index(level=0, inplace=True)

    # add marks
    mark_by_keyword_match_title = 5
    mark_by_keyword_match_desc = 3
    film_keywords = films['keywords'][film_imdb_id]
    extra_marks = recommend_by_desc(films['title'][film_imdb_id],
                                    books=books_data)
    for book_i in tqdm(books_data.index):
        book_title = books_data['title'][book_i]
        # mark = 0
        mark = extra_marks[book_title]
        book_desc = books_data['desc'][book_i]
        for film_keyword in film_keywords:
            if film_keyword in book_title:
                mark += mark_by_keyword_match_title
            if film_keyword in book_desc:
                mark += mark_by_keyword_match_desc
        books_data['mark'][book_i] += mark
    marks = pd.Series(list(books_data['mark']), index=list(books_data['title']))
    names = set(books_data['title'])
    for index in tqdm(books.index):
        if books['title'][index] in names:
            books['mark'][index] = marks[books['title'][index]]

    books_rec = books.nlargest(num_rec, 'mark')
    return books_rec
