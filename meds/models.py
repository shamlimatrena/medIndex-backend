from django.db import models
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
import os

class Med(models.Model):
    name = models.CharField(max_length=255)
    genericName = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)
    batchNumber = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='med_photos/', blank=True, null=True)

    def __str__(self):
        return self.name

# Delete the image file when the model instance is deleted
@receiver(post_delete, sender=Med)
def delete_image_on_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

# Delete the old image file when the image is updated
@receiver(pre_save, sender=Med)
def delete_image_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False
    
    try:
        old_image = Med.objects.get(pk=instance.pk).image
    except Med.DoesNotExist:
        return False
    
    new_image = instance.image
    if old_image and old_image != new_image:
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)