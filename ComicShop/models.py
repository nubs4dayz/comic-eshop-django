from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class Comic(models.Model):
    class Genre(models.TextChoices):
        ACTION = 'Action'
        ADVENTURE = 'Adventure'
        FANTASY = 'Fantasy'
        SCIFI = 'Science Fiction'
        HORROR = 'Horror'
        OTHER = 'Other'

    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    year_published = models.PositiveIntegerField()
    number_of_pages = models.PositiveIntegerField()
    quantity_in_stock = models.PositiveIntegerField()
    description = models.TextField()
    price = models.PositiveIntegerField()
    genre = models.CharField(max_length=255, choices=Genre.choices)
    cover_photo = models.ImageField(upload_to='cover_images/')

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    phone = models.CharField(max_length=9)
    address = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name} {self.surname}'


@receiver(post_save, sender=UserProfile)
def create_shopping_cart(sender, instance, created, **kwargs):
    if created:
        ShoppingCart.objects.create(dedicated_user=instance)


class ShoppingCart(models.Model):
    dedicated_user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.dedicated_user.name} {self.dedicated_user.surname}'


class ComicInOrder(models.Model):
    comic = models.ForeignKey(Comic, on_delete=models.CASCADE)
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    quantity_added = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.cart} {self.comic}'
