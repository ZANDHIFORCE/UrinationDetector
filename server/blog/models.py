from django.db import models

from django.utils import timezone   #tiemzone.now()

class Post(models.Model):
    title = models.CharField(max_length=200)
    text=models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date=models.DateTimeField(blank=True, null=True)

    LABEL_CHOICES = [
        ("UCF", "Unclassified"),
        ("URN", "Urination"),
        ("SMK", "Smoking"),
        ("ETC", "Etcetera")
    ]

    label= models.CharField(
        max_length=10, 
        choices=LABEL_CHOICES, 
        default="UCF"
    )
    
    image = models.ImageField(upload_to='intruder_image/%Y/%m/%d/', default='intruder_image/default_error.png')
    
    def publish(self):
        self.published_date=timezone.now()
        self.save()

    def get_pk(self):
        return self.id

    def __str__(self):
        return (self.title + '(' +self.label + ')')

