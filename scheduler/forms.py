"""Forms"""

from django import forms
from django.utils import timezone
from django.forms.widgets import SplitDateTimeWidget
from bootstrap_modal_forms.forms import BSModalForm

from .models import Lesson, Auditorium, Professor, Group


class SelectAuditoriumForm(forms.ModelForm):
    """ form to choose auditorium to show"""
    auditorium = forms.ModelChoiceField(queryset=Auditorium.objects.all(), to_field_name='number')

    class Meta:
        model = Auditorium
        fields: list = []


class SelectProfessorForm(forms.ModelForm):
    """ form to choose professor to show their schedule"""
    professor = forms.ModelChoiceField(queryset=Professor.objects.all(), to_field_name='id')

    class Meta:
        model = Professor
        fields: list = []


class SelectGroupForm(forms.ModelForm):
    """ form to choose group to show its schedule"""
    group = forms.ModelChoiceField(queryset=Group.objects.all(), to_field_name='id')

    class Meta:
        model = Group
        fields: list = []


class EditForm(BSModalForm):
    """ popup form to edit lessons"""
    # id is empty when creating new lesson
    id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    name = forms.CharField(max_length=100)
    start_date = forms.DateTimeField(initial=timezone.now, input_formats=['%d-%m-%Y %H:%M'],
                                     widget=SplitDateTimeWidget(date_attrs={'type': 'date'},
                                                                time_attrs={'type': 'time'}))
    end_date = forms.DateTimeField(initial=timezone.now, input_formats=['%d-%m-%Y %H:%M'],
                                   widget=SplitDateTimeWidget(date_attrs={'type': 'date'},
                                                              time_attrs={'type': 'time'}))
    auditorium = forms.CharField(max_length=100)
    group = forms.IntegerField()
    professor = forms.CharField(max_length=100)

    class Meta:
        model = Lesson
        fields: list = []
