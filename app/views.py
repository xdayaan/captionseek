from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import VideoForm
from .tasks import generate_subtitles

def home(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save()  # Save the video and get the instance
            # Trigger the Celery task
            generate_subtitles.delay(video.id, video.title)
            return redirect('video_upload_success')
    else:
        form = VideoForm()
    return render(request, 'home.html', {'form': form})

def video_upload_success(request):
    return HttpResponse("Video uploaded successfully!")
