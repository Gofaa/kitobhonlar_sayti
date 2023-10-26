from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from books.models import Book, BookReview
from users.models import CustomUser


class BookReviewAPITest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username="gofa", first_name="gafur")
        self.user.set_password("gofa")
        self.user.save()
        self.client.login(username="gofa", password="gofa")

    def test_book_review_detail(self):
        book = Book.objects.create(
            title="book1", description="description1", isbn="123123"
        )
        book_review = BookReview.objects.create(
            book=book, user=self.user, stars_given=5, comment="very good book"
        )

        response = self.client.get(
            reverse("api:review-detail", kwargs={"id": book_review.id})
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], book_review.id)
        self.assertEqual(response.data["stars_given"], 5)
        self.assertEqual(response.data["comment"], "very good book")
        self.assertEqual(response.data["book"]["id"], book_review.book.id)
        self.assertEqual(response.data["book"]["title"], "book1")
        self.assertEqual(response.data["book"]["description"], "description1")
        self.assertEqual(response.data["book"]["isbn"], "123123")
        self.assertEqual(response.data["user"]["id"], book_review.user.id)
        self.assertEqual(response.data["user"]["first_name"], "gafur")

    def test_delete_review(self):
        book = Book.objects.create(
            title="book1", description="description1", isbn="123123"
        )
        book_review = BookReview.objects.create(
            book=book, user=self.user, stars_given=5, comment="very good book"
        )

        response = self.client.delete(
            reverse("api:review-detail", kwargs={"id": book_review.id})
        )

        self.assertEqual(response.status_code, 204)
        self.assertFalse(BookReview.objects.filter(id=book_review.id).exists())

    def test_patch_review(self):
        book = Book.objects.create(
            title="book1", description="description1", isbn="123123"
        )
        book_review = BookReview.objects.create(
            book=book, user=self.user, stars_given=5, comment="very good book"
        )

        response = self.client.patch(
            reverse("api:review-detail", kwargs={"id": book_review.id}),
            data={"comment": "yaxshi book"},
        )
        book_review.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(book_review.comment, "yaxshi book")

    def test_put_review(self):
        book = Book.objects.create(
            title="book1", description="description1", isbn="123123"
        )
        book_review = BookReview.objects.create(
            book=book, user=self.user, stars_given=5, comment="very good book"
        )

        response = self.client.put(
            reverse("api:review-detail", kwargs={"id": book_review.id}),
            data={
                "stars_given": 4,
                "comment": "norm book ekan",
                "user_id": self.user.id,
                "book_id": book.id,
            },
        )
        book_review.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(book_review.stars_given, 4)
        self.assertEqual(book_review.comment, "norm book ekan")

    def test_create_review(self):
        book = Book.objects.create(
            title="book1", description="description1", isbn="123123"
        )
        data = {
            "stars_given": 3,
            "comment": "boladi, yomonmas",
            "user_id": self.user.id,
            "book_id": book.id,
        }

        response = self.client.post(reverse("api:reviews"), data=data)
        br = BookReview.objects.get(book=book)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(br.stars_given, 3)
        self.assertEqual(br.comment, "boladi, yomonmas")

    def test_book_list_review(self):
        user_two = CustomUser.objects.create(username="somebody", first_name="somebody")
        book = Book.objects.create(
            title="book1", description="description1", isbn="123123"
        )
        book_review = BookReview.objects.create(
            book=book, user=self.user, stars_given=5, comment="very good book"
        )
        book_review_two = BookReview.objects.create(
            book=book, user=user_two, stars_given=3, comment="not bad"
        )

        response = self.client.get(reverse("api:reviews"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(response.data["results"][0]["id"], book_review_two.id)
        self.assertEqual(response.data["results"][1]["id"], book_review.id)
        self.assertEqual(
            response.data["results"][0]["stars_given"], book_review_two.stars_given
        )
        self.assertEqual(
            response.data["results"][1]["stars_given"], book_review.stars_given
        )
        self.assertEqual(
            response.data["results"][0]["comment"], book_review_two.comment
        )
        self.assertEqual(response.data["results"][1]["comment"], book_review.comment)
        self.assertEqual(
            response.data["results"][0]["user"]["first_name"],
            book_review_two.user.first_name,
        )
        self.assertEqual(response.data["results"][1]["user"]["first_name"], "gafur")
