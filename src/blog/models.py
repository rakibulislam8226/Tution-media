from django.db import models
from django.utils.timezone import now

from PIL import Image
from multiselectfield import MultiSelectField

from django.contrib.auth.models import User

# Create your models here.


class Feedback(models.Model):
    name = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=30)
    complain = models.TextField(max_length=500)

    def __str__(self):
        return self.name


class Contact(models.Model):
    email = models.EmailField(max_length=30)
    phone = models.CharField(max_length=15)
    details = models.TextField(max_length=500)

    def __str__(self):
        return self.email


class Class_in(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Post(models.Model):
    CAT = (
        ("Teacher", "Teacher"),
        ("Student", "Student"),
        ("Gurdian", "Gurdian"),
        ("Instituate", "Instituate"),
    )
    SUBJECT = (
        ("Bangla", "Bangla"),
        ("English", "English"),
        ("Hindi", "Hindi"),
        ("Urdu", "Urdu"),
        ("Arabic", "Arabic"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    email = models.EmailField()
    salary = models.FloatField()
    avaliable = models.BooleanField()
    category = models.CharField(max_length=200, choices=CAT)
    image = models.ImageField(upload_to="blog/images", default="avater.jpg")
    date_time = models.DateTimeField(default=now)
    subject = MultiSelectField(
        default="Bangla", choices=SUBJECT, max_length=500, max_choices=4
    )
    class_in = models.ManyToManyField(Class_in, related_name="class_set")
    district = models.CharField(max_length=20, null=True, blank=True)

    likes = models.ManyToManyField(User, related_name="post_likes")
    views = models.ManyToManyField(User, related_name="post_views")

    def total_likes(self):
        return self.likes.count()

    def total_views(self):
        return self.views.count()

    def __str__(self):
        return self.title

    def save(self):
        super().save()
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(default=now)

    def __str__(self) -> str:
        return self.user.username + ": " + self.text[0:15]
