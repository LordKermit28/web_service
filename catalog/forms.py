from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from catalog.models import Blog, Product, Version


class BlogForm(forms.ModelForm):

    class Meta:
        model = Blog
        fields = ('title', 'content', 'preview')
        # exclude = ('published_status',)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'image', 'category', 'price',)
        exclude = ('published_status',)
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        ban_list = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
        for word in ban_list:
            if word in name:
                raise forms.ValidationError('You utilized a banned word')

        return cleaned_data

class StaffProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['status', 'description', 'category']


class VersionForm(forms.ModelForm):
    class Meta:
        model = Version
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


