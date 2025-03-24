from django.db import models

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
