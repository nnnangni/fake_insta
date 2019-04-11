from django import forms
from .models import Post, Image, Comment

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
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # fields = '__all__' # 입력을 받을 수 있도록 사용자에게 보여주는 곳    
        fields = ['content',] # content만 입력받으면 되기 때문에!!!!!!!!!!
    