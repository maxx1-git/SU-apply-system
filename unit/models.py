from django.db import models

# Create your models here.

class Classes(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, default="#000000")
    def __str__(self):
        return self.name



class Members(models.Model):
    name = models.CharField(max_length=100)
    rank = models.CharField(max_length=100)
    position = models.CharField(max_length=100, blank=True)

    class_level = models.ForeignKey(
        Classes,
        on_delete=models.PROTECT
    )
    
    def __str__(self):
        return self.name