import os
from dotenv import load_dotenv
from django.db import models
import cloudinary
import cloudinary.uploader
from cloudinary.models import CloudinaryField
from django.dispatch import receiver
from django.db.models.signals import post_delete, pre_save
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

    @property
    def image_url(self):
        """
        Generate full Cloudinary URL using cloud name from environment variable
        """
        # Get Cloudinary cloud name from environment variable
        cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME')
        
        if not self.image or not cloud_name:
            return None
        
        # Extract the path from Cloudinary's URL
        path = self.image.url.split('upload/')[-1]

        # Construct full URL with Cloudinary cloud name from env
        return f"https://res.cloudinary.com/{cloud_name}/image/upload/{path}"

    def __str__(self):
        return self.name

@receiver(post_delete, sender=Med)
def delete_cloudinary_image(sender, instance, **kwargs):
    """
    Delete image from Cloudinary when model instance is deleted
    """
    if instance.image:
        try:
            cloudinary.uploader.destroy(instance.image.public_id)
        except Exception as e:
            logger.error(f"Cloudinary deletion error: {str(e)}")

@receiver(pre_save, sender=Med)
def replace_cloudinary_image(sender, instance, **kwargs):
    """
    Delete old Cloudinary image when a new image is uploaded
    """
    if not instance.pk:
        return

    try:
        old_instance = Med.objects.get(pk=instance.pk)
        
        # Check if image has changed
        if (old_instance.image and 
            instance.image and 
            old_instance.image.public_id != instance.image.public_id):
            cloudinary.uploader.destroy(old_instance.image.public_id)
    except Med.DoesNotExist:
        pass
    except Exception as e:
        logger.error(f"Image replacement error: {str(e)}")