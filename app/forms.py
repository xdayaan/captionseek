from django import forms
from .models import Video

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'video_file']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter video title'}),
            'video_file': forms.ClearableFileInput(attrs={'placeholder': 'Choose a video file'}),
        }
