from django.db import models
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
import cloudinary
import cloudinary.uploader
from cloudinary.models import CloudinaryField
from django.conf import settings

class Med(models.Model):
    name = models.CharField(max_length=255)
    genericName = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)
    batchNumber = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = CloudinaryField('image', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.image:
            cloud_name = settings.CLOUDINARY_CLOUD_NAME  # Read from .env
            self.image_url = f"https://res.cloudinary.com/{cloud_name}/{self.image}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# Delete the image from Cloudinary when the model instance is deleted
@receiver(post_delete, sender=Med)
def delete_image_on_delete(sender, instance, **kwargs):
    if instance.image:
        cloudinary.uploader.destroy(instance.image.public_id)

# Delete old image when a new one is uploaded
@receiver(pre_save, sender=Med)
def delete_image_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return  # Skip if the instance is new

    try:
        old_instance = Med.objects.get(pk=instance.pk)
    except Med.DoesNotExist:
        return

    if old_instance.image and old_instance.image != instance.image:
        cloudinary.uploader.destroy(old_instance.image.public_id)
