from django.contrib import admin
from .models import User, RootUserAdditional, IAMUserAdditional
from django.contrib.auth.admin import UserAdmin
# Register your models here.
class UserAdmin(UserAdmin):
    # add_form = UserCreationForm
    # form = UserChangeForm
    model = User
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'name','type')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions',)}),   #'is_customer' , 'is_seller'
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'name', 'type', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
admin.site.register(User, UserAdmin)
admin.site.register(RootUserAdditional)
admin.site.register(IAMUserAdditional)