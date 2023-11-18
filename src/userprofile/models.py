from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.


class UserProfile(models.Model):
    BLOOD_GROUP = (
        ("A+", "A+"),
        ("A-", "A-"),
        ("AB+", "AB+"),
        ("AB-", "AB-"),
        ("B+", "B+"),
        ("B-", "B-"),
        ("O+", "O+"),
        ("O-", "O-"),
    )
    GENDER = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Others", "Others"),
    )
    PROFESSION = (
        ("Serviceman", "Serviceman"),
        ("Businessman", "Businessman"),
        ("Worker", "Worker"),
        ("Others", "Others"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    gender = models.CharField(max_length=6, choices=GENDER)
    address = models.CharField(max_length=40)
    date_of_birth = models.DateField()
    religion = models.CharField(max_length=10)
    nationality = models.CharField(max_length=15)
    blood_group = models.CharField(max_length=10, choices=BLOOD_GROUP)
    biodata = models.TextField()
    profession = models.CharField(max_length=15, choices=PROFESSION)
    image = models.ImageField(upload_to="userprofile/images", default="avater.jpg")

    def __str__(self):
        return f"{self.user.username} Profile"

    def save(self):
        super().save()
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
