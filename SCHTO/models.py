from django.db import models
from django.db.models.fields import DateTimeField

class Blog(models.Model):
    title = models.TextField()
    description = models.TextField()
    tags = models.TextField(null=True, blank=True)
    image = models.TextField()
    published = models.IntegerField(default=0)
    views = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    created_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)

class Board(models.Model):
    fullname = models.TextField()
    address = models.TextField()
    designation = models.TextField()
    phone = models.TextField()
    image = models.TextField()
    value = models.IntegerField(null=True, blank=True)
    gender = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    deleted_at = models.DateTimeField(null=True, blank=True)

class Payment(models.Model):
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    razorpay_payment_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Sponsor(models.Model):
    image = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Testimonial(models.Model):
    fullname = models.TextField()
    image = models.TextField()
    organization = models.TextField(null=True, blank=True)
    designation = models.TextField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    deleted_at = models.DateTimeField(null=True, blank=True)

class User(models.Model):
    name = models.TextField(null=True, blank=True)
    username = models.TextField()
    email = models.TextField(null=True, blank=True)
    password = models.TextField()
    remeber_token = models.TextField(null=True, blank=True)
    timestamp = models.TimeField(null=True, blank=True)

class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email