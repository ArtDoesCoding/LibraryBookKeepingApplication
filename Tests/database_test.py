import unittest
import sqlite3
from database import initialize_db, add_book, query_books_by_author, \
    query_books_by_title, get_all_books, remove_book


class TestDatabaseFunctions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        initialize_db()
        cls.conn = sqlite3.connect('library.db')
        cls.cursor = cls.conn.cursor()
        cls._ensure_table_exists()

    @classmethod
    def _ensure_table_exists(cls):
        cls.cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER,
            isbn TEXT
        )
        ''')
        cls.conn.commit()

    def setUp(self):
        self.cursor.execute('DELETE FROM books')
        self.conn.commit()

    def test_add_book(self):
        add_book('Test Book', 'Test Author', 2023, '1234567890')
        self.cursor.execute('SELECT * FROM books WHERE title = ?', ('Test Book',))
        book = self.cursor.fetchone()
        self.assertIsNotNone(book)
        self.assertEqual(book[1], 'Test Book')
        self.assertEqual(book[2], 'Test Author')

    def test_query_books_by_author(self):
        add_book('Test Book 1', 'Author 1', 2023, '1234567890')
        add_book('Test Book 2', 'Author 2', 2023, '1234567891')
        books = query_books_by_author('Author 1')
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0][2], 'Author 1')

    def test_query_books_by_title(self):
        add_book('Test Book 1', 'Author 1', 2023, '1234567890')
        add_book('Test Book 2', 'Author 2', 2023, '1234567891')
        books = query_books_by_title('Test Book 2')
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0][1], 'Test Book 2')

    def test_get_all_books(self):
        add_book('Test Book 1', 'Author 1', 2023, '1234567890')
        add_book('Test Book 2', 'Author 2', 2023, '1234567891')
        books = get_all_books()
        self.assertEqual(len(books), 2)

    def test_remove_book(self):
        add_book('Test Book', 'Test Author', 2023, '1234567890')
        self.cursor.execute('SELECT * FROM books WHERE title = ?', ('Test Book',))
        book = self.cursor.fetchone()
        remove_book(book[0])
        self.cursor.execute('SELECT * FROM books WHERE title = ?', ('Test Book',))
        book = self.cursor.fetchone()
        self.assertIsNone(book)

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()