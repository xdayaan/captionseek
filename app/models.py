from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=100)
    video_file = models.FileField(upload_to='videos/')

    def __str__(self):
        return self.title
    
class Videodb:
    id = models.UUIDField(primary_key=True)
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=1000)
    subtitles = models.TextField()

    class Meta:
        managed = False 
        db_table = 'captionseek'