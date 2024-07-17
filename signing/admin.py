from django.contrib import admin
from django import forms
# Register your models here.
from .models import Signing, SignatureDatabase, SigningField


class SigningAdminInline(admin.StackedInline):
    model = SigningField


class SigningAdmin(admin.ModelAdmin):
    inlines = [SigningAdminInline]
    list_display = ['certificate', 'name', 'next_serial']


class SignatureDatabaseAdmin(admin.ModelAdmin):
    list_display = ['certificate', 'serial', 'subject_dn']


admin.site.register(Signing, SigningAdmin)
admin.site.register(SignatureDatabase, SignatureDatabaseAdmin)
