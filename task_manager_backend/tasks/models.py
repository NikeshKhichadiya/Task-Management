from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name  = models.CharField(max_length=50)
    email      = models.EmailField()
    password   = models.CharField(max_length=128)  # Store hashed passwords ideally

    class Meta:
        db_table = 'users'
    