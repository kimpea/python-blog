from django import forms
from .models import Post, PostComment

class AddPostForm(forms.ModelForm):
    class Meta: 
        model = Post
        fields = ('title', 'body', 'topic')

class PostCommentForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(
        attrs={'rows': '4', 'cols': '5'}))

    class Meta:
        model = PostComment
        fields = ['comment']