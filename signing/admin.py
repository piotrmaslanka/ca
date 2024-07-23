from django.contrib import admin

from .models import Signing, SigningField


class SigningAdminInline(admin.StackedInline):
    model = SigningField
    extra = 0


class SigningAdmin(admin.ModelAdmin):
    inlines = [SigningAdminInline]
    list_display = ['certificate', 'name', 'next_serial']


admin.site.register(Signing, SigningAdmin)
