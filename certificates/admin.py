from django.contrib import admin, messages
from django.views.generic.detail import DetailView
from django import forms
from django.shortcuts import redirect, render
from .models import Certificate
from signing.models import Signing
from signing.models import SignatureDatabase


class SignatureDatabaseAdmin(admin.StackedInline):
    model = SignatureDatabase

class CertificateAdmin(admin.ModelAdmin):
    actions = ['generate_new']
    list_display = ['common_name', 'serial', 'can_sign']
    inlines = [SignatureDatabaseAdmin]

    @admin.action
    def generate_new(modeladmin, request, queryset):
        if len(queryset) != 1:
            messages.add_message(request, messages.ERROR, 'Can select at most one certificate!')
            return redirect('/admin/certificates/certificate/')
        cert, = queryset
        return redirect(f'/admin/certificates/generate/{cert.id}/')

admin.site.register(Certificate, CertificateAdmin)

