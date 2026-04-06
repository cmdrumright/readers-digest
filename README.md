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
