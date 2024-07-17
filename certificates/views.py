from django.contrib import messages
from django import forms
from django.shortcuts import render, redirect
from .models import Certificate
from signing.models import Signing
from .generator import new_certificate
from django.contrib.auth.decorators import login_required
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType


@login_required()
def generate_new(request, certificate_id: int):
    cert = Certificate.objects.get(id=certificate_id)
    if not cert.can_sign:
        messages.error(request, "You need a certificate that can sign other certificates")
        return redirect('/admin/certificates/')

    class_dict = {'c': forms.CharField(label='Country'),
                  'o': forms.CharField(label='Organisation'),
                  'ou': forms.CharField(label='Organisation unit'),
                  'cn': forms.CharField(label='Common name')}

    try:
        signing = Signing.objects.get(certificate=cert)
    except Signing.DoesNotExist:
        raise

    for field in signing.signingfield_set.all():
        class_dict[field.name.lower()] = forms.CharField(label=field.name)

    NewCertificateForm = type('NewCertificateForm', (forms.Form,), class_dict)

    if request.method == 'POST':
        form = NewCertificateForm(request.POST)
        if form.is_valid():

            kwargs = {}
            for field in signing.signingfield_set.all():
                kwargs[field.name.lower()] = form.cleaned_data[field.name.lower()]

            new_cert = new_certificate(cert, country=form.cleaned_data['c'],
                            organisation=form.cleaned_data['o'], org_unit=form.cleaned_data['ou'],
                            common_name=form.cleaned_data['cn'], **kwargs)
            messages.add_message(request, messages.SUCCESS, 'New certificate issued')
            le = LogEntry(user=request.user,
                          content_type=ContentType.objects.get(app_label='certificates', model='certificate'),
                          object_id=new_cert.id,
                          object_repr=str(new_cert),
                          action_flag=1,
                          change_message='New certificate generated')
            le.save()
            return redirect(f'/admin/certificates/certificate/{new_cert.id}/change/')
    else:
        form = NewCertificateForm()

    return render(request, 'admin/new_certificate.html', {'form': form,
                                                          'certificate': cert})

