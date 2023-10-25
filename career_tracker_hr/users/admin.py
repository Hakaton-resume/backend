from django.contrib import admin

from .models import Company, HRUser,  STAFF, StudentUser, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display =(
        'id',
        # 'username',
        'first_name',
        'last_name',
        'email',
    )


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    # list_display =(
    #     'id',
    #     'username',
    #     'first_name',
    #     'last_name',
    #     'email',
    # )
    pass
