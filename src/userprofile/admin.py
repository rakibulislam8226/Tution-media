from django.contrib import admin
from .models import UserProfile


# custom Admin site start #
class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ("user", "email", "phone")
    list_display = ("user", "email", "phone", "nationality")
    list_filter = ("blood_group", "profession", "nationality", "gender")
    search_fields = ("user", "email", "phone", "nationality", "address")


# custom Admin site end #


# Register your models here.
admin.site.register(UserProfile, ProfileAdmin)
