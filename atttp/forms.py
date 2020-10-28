from django import forms
from atttp.models import GameHead, GameDetail, Igrisce
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Field, Div, ButtonHolder, Submit, HTML, Row, Column
from crispy_forms.bootstrap import InlineRadios, UneditableField, FormActions
#from tempus_dominus.widgets import DateTimePicker
from .custom_layout_object import Formset
from django.contrib.admin import widgets
from django.contrib.auth.models import User, Group

import re

##########################################################
#  Forms
##########################################################

#GameDetailForm
class GameDetailForm(forms.ModelForm):
    
    class Meta:
        model = GameDetail
        exclude = ()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #formtag_prefix = re.sub('-[0-9]+$', '', kwargs.get('prefix', ''))

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_labels = False
        #self.helper.label_class = 'col-md-2 create-label'
        self.helper.layout = Layout(
            Div(
                InlineRadios('niz', css_class="col-md-12"), 
                HTML('<label class="create-label">Rezultat* </label>'),
                Row(
                    Field('rezultat_1', style="width: 80px"),
                    HTML('&nbsp;-&nbsp;'), 
                    Field('rezultat_2', style="width: 80px"),
                    HTML("&nbsp;"),
                    Field('max_break_point', style="width: 80px", placeholder="break"),
                ),
                HTML("<hr style='border-width: 1px'>"),
                #css_class='formset_row-{}'.format(formtag_prefix)
            ),
        )
        self.fields['max_break_point'].label = 'Break'
    '''
    TODO: date > NOW -> rezultat cannot be entered
    '''
    def clean(self):
        cleaned_data = super().clean()

        #niz = cleaned_data.get("niz")
        rezultat_1 = cleaned_data.get("rezultat_1")
        rezultat_2 = cleaned_data.get("rezultat_2")
        max_break_point = cleaned_data.get("max_break_point")

        rezultat_present = rezultat_1 and rezultat_2

        if (rezultat_1 and not rezultat_2) or (not rezultat_1 and rezultat_2):
            raise forms.ValidationError("Vnešena morata biti ali oba rezultata, ali nobeden!")
        
        if rezultat_present:
            if (rezultat_1 < 0 or rezultat_1 > 8) and (rezultat_2 < 0 or rezultat_2 > 8):
                raise forms.ValidationError("Rezultat je lahko le število med 1 in 7!")

            if ((max_break_point and max_break_point < 0) or 
                (rezultat_1 and rezultat_1 < 0) or
                (rezultat_2 and rezultat_2 < 0)):
                raise forms.ValidationError("Rezultat mora biti pozitivno število!")
        
        if (not rezultat_present and max_break_point) or \
            (max_break_point and (rezultat_1 != 7 or rezultat_2 != 7)):
            raise forms.ValidationError("Break je lahko vnešen le ob pogoju, da je rezultat 7-6!")
        
        
        return cleaned_data
    

#Create inline formset
GameDetailInlineFormSet = inlineformset_factory(GameHead,
    GameDetail,
    form=GameDetailForm,
    fields=['niz', 'rezultat_1', 'rezultat_2', 'max_break_point'],
    extra=0,
    can_delete=False,
    )

#GameHeadForm
class GameHeadForm(forms.ModelForm):

    class Meta:
        model = GameHead
        fields = ('club',
                'datum',
                'igrisce',
                'oseba_1',
                'oseba_2')
        
        '''
        field_classes = {
            'datum': forms.SplitDateTimeField,
        }
        widgets = {
            'datum': forms.SplitDateTimeWidget(
                date_attrs={'class': 'datepicker'},
                time_attrs={'class': 'timepicker'},

                date_format='%d/%m/%Y',
                time_format='%H:%M'
            ),
        }
        '''
    club = forms.ChoiceField(required=False)
    datum = forms.SplitDateTimeField(input_date_formats=['%d/%m/%Y'], input_time_formats=['%H:%M'],
                                    widget=forms.SplitDateTimeWidget(date_format='%d/%m/%Y',
                                                                     time_format='%H:%M',
                                                                     date_attrs={'class': 'datepicker'},
                                                                     time_attrs={'class': 'timepicker'}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')

        super().__init__(*args, **kwargs)


        #Populate clubs dropdown based on current user
        clubs = Group.objects.filter(user=self.user)
        club_list = [('     ', '     ')]
        for c in clubs:
            club_list.append((c.name, c.name))
        #club_list = club_list.append(list((c.id,c.name) for c in clubs))
        self.fields['club'].choices = club_list

        #get users in the same group as selected (1st) group
        users_qs = User.objects.filter(groups__name__in=[club_list[0][0]])
        user_list = list((u.id, u.first_name) for u in users_qs)
        self.fields['oseba_1'].choices = user_list
        self.fields['oseba_2'].choices = user_list

        self.fields['club'].label = 'Klub'
        self.fields['igrisce'].label = 'Igrišče'
        self.fields['oseba_1'].label = ' '
        self.fields['oseba_2'].label = ' '

        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2 create-label'
        #self.helper.field_class = 'col-md-6'
        self.helper.layout = Layout(
            Fieldset(
                'Klub',
                'club'
            ),
            Fieldset(
                'Igra',
                Div(Field('datum', autocomplete='off'),
                    Field('igrisce')
                ),
            ),
            Fieldset('Tekmovalca',
                     Row(Field('oseba_1'),
                        HTML("&emsp;"),
                        Field('oseba_2')
                     ),
            FormActions(
                        Submit('submit', 'Shrani')
                    ),
            ),
            '''
            HTML('<form method="post">'),
            HTML('{% csrf_token %}'),
            Fieldset('Nizi',
                     Formset('details'),
                     HTML("<hr style='border-width: 1px'>"),
                     FormActions(
                            Submit('submit', 'Shrani')
                        ),
            ),
            HTML('</form>')
            '''
        )


    def clean(self):
        cleaned_data = super().clean()

        oseba_1 = cleaned_data.get('oseba_1')
        oseba_2 = cleaned_data.get('oseba_2')

        if oseba_1 and oseba_2:
            if oseba_1.username == oseba_2.username:
                raise forms.ValidationError("Igralca ne moreta biti ista oseba!")
        
        return cleaned_data
    

##########################################################
#  FormHelpers
##########################################################

class GameFilterFormHelper(FormHelper):
    model = GameHead
    form_tag = False

    layout = Layout('Sezona', ButtonHolder(
        Submit('submit', 'Osveži', css_class='btn btn-dark')
    ))