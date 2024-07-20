from django import forms
from .models import User, Post, Profile, Like

class NewPost(forms.Form):
    post= forms.Field(widget=forms.Textarea(
        {'rows': '3', 'maxlength': 480, 'class': 'form-control', 'placeholder': "What do you want to share?"}), label="New Post", required=True)


class EditPost(forms.Form):
    id_form_edit = forms.Field(widget=forms.Textarea(
        {'rows': '3', 'maxlength': 480, 'class': 'form-control', 'id': 'id_form_edit'}), label="New Post", required=True)
     