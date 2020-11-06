from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from blogApp.models import User,Blogs,Comment


# Register your models here.


class BaseUserAdmin(UserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'dob']
    search_fields = ['__all__']
    readonly_fields = (
        'date_joined',
        'last_login',
    )

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'dob', 'password1', 'password2'),
        }),
    )
    ordering = ()
    exclude = []


admin.site.register(User, BaseUserAdmin)
admin.site.register(Blogs)
admin.site.register(Comment)
