from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class Post(models.Model):
    STATUS_CHOICES = (
        ('published', 'Published'),
        ('draft', 'Draft'),
    )
    title = models.CharField(max_length=200)
    text = models.TextField()
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=10)
    slug = models.SlugField(max_length=250, blank=False, editable=False)
    cover = models.ImageField(upload_to='post_cover/', blank=True)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        kwargs = {
            'slug' : self.slug,
            'pk' : self.id,
        }
        return reverse('post_detail', kwargs=kwargs)
        
    def get_absolute_update_url(self):
        kwargs = {
            'slug' : self.slug,
            'pk' : self.id,
        }
        return reverse('post_update', kwargs=kwargs)

    def get_absolute_delete_url(self):
        kwargs = {
            'slug' : self.slug,
            'pk' : self.id,
        }
        return reverse('post_delete', kwargs=kwargs)

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode = True)
        super().save(*args, **kwargs)
    

    
