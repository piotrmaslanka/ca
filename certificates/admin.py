from django.contrib import admin, messages
from django.shortcuts import redirect

from signing.models import SignatureDatabase
from .models import Certificate

admin.site.site_title = "CA: Certificate Authority"
admin.site.site_header = 'CA: Certificate Authority'
admin.site.index_title = 'CA: Certificate Authority'


class SignatureDatabaseAdmin(admin.TabularInline):
    model = SignatureDatabase
    readonly_fields = (
    'expiration', 'serial', 'subject_dn', 'certificate', 'signing', 'status', 'revocation', 'signed_by')
    fields = ('expiration', 'serial', 'subject_dn', 'certificate')
    extra = 0
    can_delete = False
    fk_name = 'signed_by'
    verbose_name = 'Database of signatures'


class CertificateAdmin(admin.ModelAdmin):
    actions = ['generate_new']
    readonly_fields = ['serial', 'signed_by', 'extra_data', 'issuer']
    fields = ['public_key', 'private_key', 'is_used_for_client_auth', 'is_ca', 'can_sign',
              'common_name', 'signed_by', 'serial', 'extra_data', 'issuer']
    list_display = ['common_name', 'serial', 'can_sign']
    inlines = [SignatureDatabaseAdmin]

    @admin.action
    def generate_new(modeladmin, request, queryset):
        if queryset.count() != 1:
            messages.add_message(request, messages.ERROR, 'Can select at most one certificate!')
            return redirect('/admin/certificates/certificate/')
        cert, = queryset
        return redirect(f'/admin/certificates/generate/{cert.id}/')


admin.site.register(Certificate, CertificateAdmin)
