from django.db import models

# Create your models here.
class Camera(models.Model):

    ip = models.CharField(
		max_length=200, blank=False, null=False)
    port = models.CharField(max_length=200, blank=False)
    password = models.CharField(max_length=200, blank=False)
    username = models.CharField(max_length=200, blank=False)


    def __str__(self):
	    return self.ip

    def save(self, *args, **kwargs):
	    super(Camera, self).save(*args, **kwargs)