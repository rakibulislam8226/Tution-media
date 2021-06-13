from django import forms
from django.db.models import fields
from django.forms import widgets
from . models import Contact, Post
from . fields import ListTextWidget

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = {'user','id', 'date_time','likes','views'}
        widgets={
            'class_in':forms.CheckboxSelectMultiple(attrs={'multiple':True,})
        }
    def __init__(self,*args, **kwargs):
        _district_set=kwargs.pop('district_set',None)
        super(CreatePostForm,self).__init__(*args, **kwargs)
        self.fields['district'].widget=ListTextWidget(data_list=_district_set,name='district-set')










