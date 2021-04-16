from django import forms
from .models import Student

class Student_form(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'powerschool_id',
            'first_name',
            'last_name',
            'grade',
            'gender',
            'islamic',
            'behavior',
            'friend1',
            'friend2',
            'friend3',
            'friend4',
            'friend5',
        ]


