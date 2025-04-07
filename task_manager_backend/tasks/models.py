from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name  = models.CharField(max_length=50)
    email      = models.EmailField(unique=True)
    password   = models.CharField(max_length=128)
    
    class Meta:
        db_table = 'users'  # Store hashed passwords ideally