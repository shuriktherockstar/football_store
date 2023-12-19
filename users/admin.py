from django.contrib import admin

from users.models import User, Profile, Address


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


admin.site.register(Profile)
admin.site.register(Address)
