from django.db import models
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
import cloudinary
import cloudinary.uploader
from cloudinary.models import CloudinaryField
from django.conf import settings
import logging

# Set up logger
logger = logging.getLogger(__name__)

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
        try:
            if self.image and hasattr(self.image, 'url'):
                # Use Cloudinary's built-in URL method instead of manual construction
                self.image_url = self.image.url
            super().save(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error saving Med model: {str(e)}")
            raise

    def __str__(self):
        return self.name

# Delete the image from Cloudinary when the model instance is deleted
@receiver(post_delete, sender=Med)
def delete_image_on_delete(sender, instance, **kwargs):
    if instance.image and hasattr(instance.image, 'public_id'):
        try:
            logger.info(f"Deleting image with public_id: {instance.image.public_id}")
            result = cloudinary.uploader.destroy(instance.image.public_id)
            if result.get('result') != 'ok':
                logger.warning(f"Cloudinary deletion issue: {result}")
        except Exception as e:
            logger.error(f"Error deleting image from Cloudinary: {str(e)}")

# Delete old image when a new one is uploaded
@receiver(pre_save, sender=Med)
def delete_image_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return  # Skip if the instance is new

    try:
        old_instance = Med.objects.get(pk=instance.pk)
    except Med.DoesNotExist:
        return

    # Check if image exists and has changed
    if (old_instance.image and hasattr(old_instance.image, 'public_id') and 
            (not instance.image or old_instance.image.public_id != getattr(instance.image, 'public_id', None))):
        try:
            logger.info(f"Replacing image with public_id: {old_instance.image.public_id}")
            result = cloudinary.uploader.destroy(old_instance.image.public_id)
            if result.get('result') != 'ok':
                logger.warning(f"Cloudinary deletion issue: {result}")
        except Exception as e:
            logger.error(f"Error replacing image in Cloudinary: {str(e)}")

# Ensure Cloudinary is properly configured at module load time
def check_cloudinary_config():
    try:
        required_settings = ['CLOUDINARY_CLOUD_NAME', 'CLOUDINARY_API_KEY', 'CLOUDINARY_API_SECRET']
        missing = [s for s in required_settings if not hasattr(settings, s)]
        if missing:
            logger.error(f"Missing Cloudinary settings: {', '.join(missing)}")
    except Exception as e:
        logger.error(f"Error checking Cloudinary configuration: {str(e)}")

# Run configuration check
check_cloudinary_config()