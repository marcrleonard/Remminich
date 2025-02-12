from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.html import format_html

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import CustomUser
from django.urls import reverse


admin.site.site_header = "Admin Portal"
admin.site.site_title = "Admin Portal"
admin.site.index_title = "Welcome to the Admin Portal"


@admin.register(CustomUser)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'user_job' , 'subscription_level')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'subscription_level'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'subscription_level')
    search_fields = ('email', 'first_name', 'last_name', 'subscription_level')
    ordering = ('email',)
    readonly_fields = ('email', 'first_name', 'last_name', )

# admin.site.unregister(User)

# from .models import CustomUser
# # Register your models here.
#
# admin.site.register(CustomUser)
