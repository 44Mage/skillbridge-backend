from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Subscription, Transaction

# Register the User (using the default helper)
admin.site.register(User, UserAdmin)

# Register the other tables
admin.site.register(Subscription)
admin.site.register(Transaction)
