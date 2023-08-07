from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=[('AVAILABLE', 'Available'), ('BORROWED', 'Borrowed')], default='AVAILABLE')
    def __str__(self):
        return self.title
class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=[('LIBRARIAN', 'Librarian'), ('MEMBER', 'Member')])
    def __str__(self):
        return self.username