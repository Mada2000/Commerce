from django.contrib import admin
from .models import listing, Bid, comment

admin.site.register(listing)
admin.site.register(Bid)
admin.site.register(comment)

