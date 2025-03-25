import os
from dotenv import load_dotenv
from django.db import models
import cloudinary
import cloudinary.uploader
from cloudinary.models import CloudinaryField
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
import logging

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class Med(models.Model):
    name = models.CharField(max_length=255)
    genericName = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)
    batchNumber = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = CloudinaryField('image', blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Generate full Cloudinary URL if image exists
        if self.image:
            cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME')
            if cloud_name:
                # Extract the path from Cloudinary's URL
                path = self.image.url.split('upload/')[-1]
                # Construct full URL
                self.image_url = f"https://res.cloudinary.com/{cloud_name}/image/upload/{path}"
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

@receiver(post_save, sender=Med)
def update_image_url(sender, instance, created, **kwargs):
    """
    Ensure image_url is populated even for existing instances
    """
    if instance.image and not instance.image_url:
        cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME')
        if cloud_name:
            path = instance.image.url.split('upload/')[-1]
            instance.image_url = f"https://res.cloudinary.com/{cloud_name}/image/upload/{path}"
            instance.save()

@receiver(post_save, sender=Med)
def delete_cloudinary_image(sender, instance, created, **kwargs):
    """
    Delete image from Cloudinary when model instance is deleted
    """
    if not created and instance.image:
        try:
            cloudinary.uploader.destroy(instance.image.public_id)
        except Exception as e:
            logger.error(f"Cloudinary deletion error: {str(e)}")