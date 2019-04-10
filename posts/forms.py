from django import forms
from .models import Post, Image

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # fields = '__all__'
        fields = ['content',] # content와 user의 정보를 다 보여주지 않고 content만
        
class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        # fields = '__all__'
        fields = ['file',]
        widgets = {
            'file' : forms.FileInput(attrs={'multiple':True})
        }