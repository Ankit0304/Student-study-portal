from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.
class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = RichTextUploadingField() 
    attachment = models.FileField(upload_to="pdfs/", blank=True, null=True)  # for PDF, images, slides
    
    def __str__(self):
        return self.title
    
    class Meta :
        verbose_name = 'Note'
        verbose_name_plural = 'Note'
    
class Homework(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    description = models.TextField()
    due = models.DateTimeField()
    is_finished = models.BooleanField(default=False)
     
    def __str__(self):
        return self.title
    
class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    is_finished = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
     
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True, null=True)
    cover_image = models.URLField(blank=True, null=True)  # from Google Books API
    total_pages = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class ReadingProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    current_page = models.IntegerField(default=0)
    time_spent = models.IntegerField(default=0)  # minutes
    finished = models.BooleanField(default=False)

    @property
    def progress_percent(self):
        total = self.book.total_pages or 0
        if total > 0:
            return int((self.current_page / total) * 100)
        return 0