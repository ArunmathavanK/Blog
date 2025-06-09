from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'


# Automatically delete old image when updating to a new one
@receiver(pre_save, sender=Profile)
def delete_old_image_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return  # New profile, no need to delete anything

    try:
        old_image = Profile.objects.get(pk=instance.pk).image
    except Profile.DoesNotExist:
        return

    new_image = instance.image
    if old_image and old_image.url != new_image.url:
        if old_image.name != 'default.jpg':  # Don't delete the default image
            old_image.delete(save=False)


# Automatically delete image from S3 when profile is deleted
@receiver(post_delete, sender=Profile)
def delete_image_on_delete(sender, instance, **kwargs):
    if instance.image and instance.image.name != 'default.jpg':
        instance.image.delete(save=False)

    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)