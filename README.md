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

### Using a serializer method

```py
class BookSerializer(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()
    categories = CategorySerializer(many=True)

    def get_is_owner(self, obj):
        # Check if the authenticated user is the owner
        return self.context["request"].user == obj.user

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "author",
            "isbn",
            "img_url",
            "is_owner",
            "categories",
        ]
```

### Setting the many-to-many values on create

```py
def create(self, request):
        # Get the data from the client's JSON payload
        title = request.data.get("title")
        author = request.data.get("author")
        isbn = request.data.get("isbn")
        img_url = request.data.get("img_url")

        # Create a book database row first, so you have a
        # primary key to work with
        book = Book.objects.create(
            user=request.user,
            title=title,
            author=author,
            img_url=img_url,
            isbn=isbn,
        )

        # Establish the many-to-many relationships
        category_ids = request.data.get("categories", [])
        book.categories.set(category_ids)

        serializer = BookSerializer(book, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
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
curl --header "Authorization: Token d74b97fbe905134520bb236b0016703f50380dcf" \
--request "DELETE" \
'http://localhost:8000/books/2' | jq

```

### Update a book ?

```bash
curl --header "Content-Type: application/json"   --header "Authorization: Token ec7ddcc665035a3adeaa80ed8f812bfe3ef5b5f4"   --request PUT   --data '{
    "title": "The Neverending Story",
    "author": "Edwin R. Billows",
    "isbn": "8573282904",
    "img_url": "http://www.allbooks.com/neverendingstory/images/cover.png",
    "categories": [3, 4]
}'   'http://localhost:8000/books/3' | jq
```

```bash
curl --header "Content-Type: application/json"   --header "Authorization: Token ec7ddcc665035a3adeaa80ed8f812bfe3ef5b5f4"   --request PUT   --data '{
    "title": "The Neverending Story",
    "author": "Edwin R. Billows",
    "isbn": "8573282904",
    "img_url": "http://www.allbooks.com/neverendingstory/images/cover.png",
    "categories": [{"id":3},{"id":4}]
}'   'http://localhost:8000/books/2' | jq
```

### Create Review with categories

```bash
curl --header "Content-Type: application/json" \
  --header "Authorization: Token ec7ddcc665035a3adeaa80ed8f812bfe3ef5b5f4" \
  --request POST \
  --data '{
    "book_id": 1,
    "rating": 4,
    "comment": "A very cool book"
}' \
  'http://localhost:8000/reviews' | jq
```

### Get All Reviews

```bash
curl --header "Authorization: Token ec7ddcc665035a3adeaa80ed8f812bfe3ef5b5f4" \
'http://localhost:8000/reviews' | jq
```

### Get 1 Review

```bash
curl --header "Authorization: Token ec7ddcc665035a3adeaa80ed8f812bfe3ef5b5f4" \
'http://localhost:8000/reviews/1' | jq
```

### Delete Review

```bash
curl --header "Authorization: Token ec7ddcc665035a3adeaa80ed8f812bfe3ef5b5f4" \
--request "DELETE" \
'http://localhost:8000/reviews/1' | jq

```
