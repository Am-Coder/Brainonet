from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Account, Authi, Token, Group, MemberShip


class AccountAdmin(UserAdmin):

    list_display = ('pk', 'first_name', 'last_name', 'mobile_number', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('pk', 'mobile_number')
    readonly_fields = ('pk', 'date_joined', 'last_login')
    ordering = ('pk', 'mobile_number',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    # fields = ('pk', 'first_name', 'last_name', 'mobile_number', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    # exclude = ('username',)


admin.site.register(Account, AccountAdmin)
admin.site.register(Authi)
admin.site.register(Token)
admin.site.register(Group)
admin.site.register(MemberShip)
