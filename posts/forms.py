from django import forms
from django.forms import ModelForm, Textarea
from posts.models import Comment

class CommentForm(ModelForm):
	comment = forms.CharField(widget=forms.Textarea(attrs={'cols':80, 'rows':8}))
	class Meta:
		model = Comment
		exclude = ('status','post')