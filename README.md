# readers-digest

An NSS lesson for setting up an api with a many-to-many relationship in Django

## Lessons

### How to add a many-to-many relationship

```py
class Book(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="books_created"
    )
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=20)
    isbn = models.CharField(max_length=13, null=True, blank=True)
    img_url = models.URLField(null=True, blank=True)
    categories = models.ManyToManyField(
        "Category", through="BookCategory", related_name="books"
    )
```

### Using viewset

```py
class UserViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'], url_path='register')
    def register_account(self, request):
        ...

    @action(detail=False, methods=['post'], url_path='login')
    def user_login(self, request):
        ...

urlpatterns = [
    path('', include(router.urls)),
    path('login', UserViewSet.as_view({'post': 'user_login'}), name='login'),
    path('register', UserViewSet.as_view({'post': 'register_account'}), name='register'),
]
```

### Seeding database

add fixtures to api (books.json)

```json
[
  {
    "model": "digestapi.book",
    "pk": 1,
    "fields": {
      "title": "Dune",
      "author": "Frank Herbert",
      "isbn": "9780425080023",
      "img_url": "https://m.media-amazon.com/images/S/compressedphotogoodreads.com/books/1568298892i/117899.jpg",
      "user": 2
    }
  }
]
```

run a bash script to remake the database and load fixtures

```bash
#!/bin/bash

rm db.sqlite3
rm -rf ./digestapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations digestapi
python3 manage.py migrate digestapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata books
```

## Testing

### Register

```bash
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{
    "username": "meg@ducharme.com",
    "password": "ducharme",
    "first_name": "Meg",
    "last_name": "Ducharme"
}' \
  'http://localhost:8000/register' | jq
```

### Login

```bash
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{
    "username": "meg@ducharme.com",
    "password": "ducharme"
}' \
  'http://localhost:8000/login' | jq
```

### Get All Categories

```bash
curl --header "Authorization: Token ec7ddcc665035a3adeaa80ed8f812bfe3ef5b5f4" \
'http://localhost:8000/categories' | jq
```

### Get 1 Category

```bash
curl --header "Authorization: Token ec7ddcc665035a3adeaa80ed8f812bfe3ef5b5f4" \
'http://localhost:8000/categories/1' | jq
```

### Get All Books

```bash
curl --header "Authorization: Token ec7ddcc665035a3adeaa80ed8f812bfe3ef5b5f4" \
'http://localhost:8000/books' | jq
```

### Create Book with categories

```bash
curl --header "Content-Type: application/json" \
  --header "Authorization: Token ec7ddcc665035a3adeaa80ed8f812bfe3ef5b5f4" \
  --request POST \
  --data '{
    "title": "The Neverending Story",
    "author": "Edwin R. Billows",
    "isbn": "8573282904",
    "img_url": "http://www.allbooks.com/neverendingstory/images/cover.png",
    "categories": [3, 5]
}' \
  'http://localhost:8000/books' | jq
```

### Delete Book

```bash
curl --header "Authorization: Token ec7ddcc665035a3adeaa80ed8f812bfe3ef5b5f4" \
--request "DELETE" \
'http://localhost:8000/books/2' | jq

```
