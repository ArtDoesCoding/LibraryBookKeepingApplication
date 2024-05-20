import PySimpleGUI as sg
from database import add_book, query_books_by_author, query_books_by_title, get_all_books, \
    remove_book

sg.LOOK_AND_FEEL_TABLE['CustomTheme'] = {
    'BACKGROUND': '#2B2B2B',
    'TEXT': '#E5E5E5',
    'INPUT': '#3C3F41',
    'TEXT_INPUT': '#E5E5E5',
    'SCROLL': '#3C3F41',
    'BUTTON': ('#E5E5E5', '#007ACC'),
    'PROGRESS': ('#D1826B', '#CC8019'),
    'BORDER': 1,
    'SLIDER_DEPTH': 0,
    'PROGRESS_DEPTH': 0,
}

sg.theme('CustomTheme')


def create_window():
    layout = [
        [sg.Text('Library Bookkeeping', size=(30, 1), justification='center',
                 font=('Helvetica', 20), relief=sg.RELIEF_RIDGE, expand_x=True)],
        [sg.HorizontalSeparator()],
        [sg.Text('Title', size=(15, 1)), sg.InputText(key='-TITLE-', size=(50, 1), expand_x=True)],
        [sg.Text('Author', size=(15, 1)),
         sg.InputText(key='-AUTHOR-', size=(50, 1), expand_x=True)],
        [sg.Text('Year', size=(15, 1)), sg.InputText(key='-YEAR-', size=(50, 1), expand_x=True)],
        [sg.Text('ISBN', size=(15, 1)), sg.InputText(key='-ISBN-', size=(50, 1), expand_x=True)],
        [sg.Button('Add Book', size=(15, 1)), sg.Button('List All Books', size=(15, 1))],
        [sg.HorizontalSeparator()],
        [sg.Text('Search by Title', size=(15, 1)),
         sg.InputText(key='-SEARCH_TITLE-', size=(50, 1), expand_x=True),
         sg.Button('Search Title', size=(15, 1))],
        [sg.Text('Search by Author', size=(15, 1)),
         sg.InputText(key='-SEARCH_AUTHOR-', size=(50, 1), expand_x=True),
         sg.Button('Search Author', size=(15, 1))],
        [sg.HorizontalSeparator()],
        [sg.Text('Search Results', size=(40, 1), font=('Helvetica', 15), justification='center')],
        [sg.Listbox(values=[], size=(80, 10), key='-RESULTS-', enable_events=True,
                    font=('Helvetica', 12), expand_x=True, expand_y=True)],
        [sg.Button('Remove Selected Book', size=(20, 1), button_color=('white', 'red'))],
        [sg.Button('Exit', size=(15, 1))]
    ]

    return sg.Window('Library Bookkeeping', layout, finalize=True, resizable=True, icon='Media'
                                                                                        '/icon.ico')


def format_book(book):
    return f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Year: {book[3]}, ISBN: {book[4]}"


def main():
    window = create_window()

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        elif event == 'Add Book':
            add_book(values['-TITLE-'], values['-AUTHOR-'], values['-YEAR-'], values['-ISBN-'])
            sg.popup('Book added successfully!', title='Success', keep_on_top=True)
        elif event == 'Search Title':
            results = query_books_by_title(values['-SEARCH_TITLE-'])
            formatted_results = [format_book(book) for book in results]
            window['-RESULTS-'].update(formatted_results)
        elif event == 'Search Author':
            results = query_books_by_author(values['-SEARCH_AUTHOR-'])
            formatted_results = [format_book(book) for book in results]
            window['-RESULTS-'].update(formatted_results)
        elif event == 'List All Books':
            results = get_all_books()
            formatted_results = [format_book(book) for book in results]
            window['-RESULTS-'].update(formatted_results)
        elif event == 'Remove Selected Book':
            selected_book = values['-RESULTS-']
            if selected_book:
                book_id = int(
                    selected_book[0].split(",")[0].split(":")[1].strip())
                remove_book(book_id)
                sg.popup('Book removed successfully!', title='Success', keep_on_top=True)
                results = get_all_books()
                formatted_results = [format_book(book) for book in results]
                window['-RESULTS-'].update(formatted_results)

    window.close()


if __name__ == '__main__':
    main()
