from django.contrib import admin
from .models import User, Category, Listing, Watch_List, Comment, Bid_Infor

# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(Watch_List)
admin.site.register(Comment)
admin.site.register(Bid_Infor)