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
