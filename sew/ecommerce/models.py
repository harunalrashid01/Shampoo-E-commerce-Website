from django.db import models

class Master(models.Model):
    name = models.CharField(max_length=100)  # Compulsory field
    img = models.ImageField(upload_to='images/', blank=True, null=True)  # Optional field for image
    category = models.CharField(max_length=50, blank=True, null=True)  # Optional field for category
    description = models.TextField(blank=True, null=True)  # Optional field for description

    def __str__(self):
        return self.name
