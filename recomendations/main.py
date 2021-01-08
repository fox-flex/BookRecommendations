"""
main module of project
"""
# from crate_recommendations import give_rec_book_by_film
import time
import warnings
from crate_recommendations import give_rec_book_by_film
try:
    books_df
except NameError:
    from books_info_read import books as books_df
try:
    films_df
except NameError:
    from films_info_read import films as films_df


warnings.filterwarnings('ignore')


def print_beauty(text: str):
    """
    slowly print text
    >>> print_beauty('Hello World!')
                               Hello World!
    """
    text = text.strip()
    len_space = 0
    len_text = len(text)
    if len_text < 66:
        if len_text % 2 == 0:
            len_space = (66 - len_text) // 2
        else:
            len_space = (65 - len_text) // 2
        text = ' ' * len_space + text
    for char in text:
        print(char, end='', flush=True)
        if char != ' ':
            time.sleep(0.)
    print()


def main(films=films_df):
    """
    main function of project
    run main program
    """
    print_beauty('Hi!')
    print_beauty('You see the film and wona to read some book in same theme?')
    print_beauty("Print 'y' if yes and something else if not.")
    if input() != 'y':
        print_beauty("No then no. By by :)")
        return
    print_beauty('Ok, then I will help to you!!!')
    run = True
    while run:
        print_beauty('Type which film you watch.')
        films_index = []
        while not films_index:
            film_keys = set(input().split())
            for index in films.index:
                for film_key in film_keys:
                    if film_key in films['title'][index].lower():
                        films_index.append(index)
            if not films_index:
                print('Name is wrong! Try again')
        films_index = list(enumerate(films_index))
        print_beauty('Print number of film which exactly you watched:')
        for val in films_index:
            print(str(val[0] + 1) + ' - ' + films['title'][val[1]])
        film = None
        while film is None:
            try:
                film = int(input('Write number: ')) - 1
                if film in {x[0] for x in films_index}:
                    film = films_index[film][1]
                else:
                    film = int('a')
            except ValueError:
                print('Number is wrong! Try again')
                film = None
        print_beauty('Wait a little bit. It will cost it :)')
        num_rec = 3
        rec = give_rec_book_by_film(film, num_rec=num_rec)
        print_beauty('Hear are recommendations for you:')
        for i in range(num_rec):
            print('Book #' + str(i + 1) + ':')
            print('Title:', rec['title'].iloc[i])
            print('Author:', rec['author'].iloc[i])
            print('Genre: ', end='')
            for genre in rec['genre'].iloc[i]:
                print(genre + '\t', end='')
            print()
            print('Rating:', str(rec['rating'].iloc[i]) + '/5')
            print('Publication date:', rec['publication_date'].iloc[i])
            print('num_pages:', rec['num_pages'].iloc[i])
            print('Description:', rec['desc'].iloc[i])
            print()
        print_beauty('As many book you will read,')
        print_beauty('as good recommendation you will have!')
        print_beauty('Will you find next book!')
        print_beauty("Print 'y' if yes and something else if not.")
        if input() != 'y':
            print_beauty("Ok! Have nice day!")
            return


main()
