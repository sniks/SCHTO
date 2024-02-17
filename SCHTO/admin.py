from django.contrib import admin
from .models import Blog, Board, Sponsor, Testimonial, Payment,NewsletterSubscription
from django.contrib.admin.models import LogEntry

admin.site.register(Blog)
admin.site.register(Board)
admin.site.register(Sponsor)
admin.site.register(Payment)
admin.site.register(NewsletterSubscription)
