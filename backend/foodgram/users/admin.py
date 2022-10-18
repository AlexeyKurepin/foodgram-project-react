from django.contrib import admin

from users.models import Subscription, User


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'username',
                    'email',
                    'first_name',
                    'last_name',
                    'is_active',
                    'last_login',
                    )
    list_editable = ('is_active',)
    search_fields = ('username', 'email')
    empty_value_display = '-пусто-'


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'user',
                    'author',
                    )
    list_editable = ('user', 'author',)
    list_filter = ('user', 'author')


admin.site.register(User, UserAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
