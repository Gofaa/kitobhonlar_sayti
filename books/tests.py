from django.test import TestCase
from django.urls import reverse

from users.models import CustomUser
from .models import Book


# Create your tests here.


class BooksTestCase(TestCase):
    def test_no_books(self):
        response = self.client.get(reverse('books:list'))
        self.assertContains(response, "No books found.")


    def test_books_list(self):
        Book.objects.create(title='Book1', description='description1', isbn='121272')
        Book.objects.create(title='Book2', description='description2', isbn='126212')
        Book.objects.create(title='Book3', description='description3', isbn='121612')
        Book.objects.create(title='Book4', description='description4', isbn='121512')

        response = self.client.get(reverse('books:list'))

        books = Book.objects.all()

        for book in books:
            self.assertContains(response, book.title)



    def test_book_detail(self):
        book = Book.objects.create(title='Book1', description='description1', isbn='121272')
        response = self.client.get(reverse('books:detail', kwargs={'id': book.id}))

        self.assertContains(response, book.title)
        self.assertContains(response, book.description)


    def test_books_search(self):
        book1 = Book.objects.create(title='ali', description="description1", isbn='1234555')
        book2 = Book.objects.create(title='vali', description="description2", isbn='1234555')
        book3 = Book.objects.create(title='gani', description="description3", isbn='1234555')

        response = self.client.get(reverse('books:list')+"?q=ali")
        self.assertContains(response, book1)


class BooksReviewsTestCase(TestCase):
    def test_add_review(self):
        book = Book.objects.create(title='book1', description='description1', isbn='1234553')
        user = CustomUser.objects.create(username='gofa', first_name='gofajan', last_name='asadov', email='gofa@gmail.com'
        )
        user.set_password('gofajan')
        user.save()
        self.client.login(username='gofa', password='gofajan')

        self.client.post(reverse('books:review', kwargs={'id': book.id}), data={
            'stars_given': 3,
            'comment': 'nice book'
        })
        book_reviews = book.bookreview_set.all()

        self.assertEqual(book_reviews.count(), 1)
        self.assertEqual(book_reviews[0].stars_given, 3)
        self.assertEqual(book_reviews[0].comment, 'nice book')
        self.assertEqual(book_reviews[0].user, user)
        self.assertEqual(book_reviews[0].book, book)
