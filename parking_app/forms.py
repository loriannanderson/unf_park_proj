from django import forms
from .models import Registration

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['student_id_num', 'employee_id_num', 'address_1', 'address_2', 'city','state','zip_code',
                  'phone', 'vehicle_make','vehicle_model',  'license_plate', 'vehicle2_make',
                  'license2_plate']

