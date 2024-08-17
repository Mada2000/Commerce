from django.contrib import admin
from .models import listing, Bid, comment, watchlist

admin.site.register(listing)
admin.site.register(Bid)
admin.site.register(comment)
admin.site.register(watchlist)

