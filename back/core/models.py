from django.db import models


class Image(models.Model):
    image_id = models.AutoField(primary_key=True)
    url = models.URLField(max_length=200)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class User(models.Model):
    user_id = models.CharField(max_length=100, primary_key=True)
    email = models.EmailField(unique=True)
    alias = models.CharField(max_length=150)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    birthdate = models.DateField(blank=True, null=True)
    profile_picture = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.email
