from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import ProductImage
import os

# @receiver(post_delete, sender=ProductImage)
# def photo_post_delete_handler(sender, **kwargs):
#     photo = kwargs['instance']
#     if photo.image:
#         storage, path = photo.image.storage, photo.image.path
#         storage.delete(path)

@receiver(post_delete, sender=ProductImage)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `ProductImage` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

@receiver(pre_save, sender=ProductImage)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `ProductImage` object is updated
    with new file.
    """
    if not instance.pk:
        return False
    try:
        old_file = ProductImage.objects.get(pk=instance.pk).image
    except ProductImage.DoesNotExist:
        return False

    new_file = instance.image
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)