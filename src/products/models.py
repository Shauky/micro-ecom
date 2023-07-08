import pathlib
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.urls import reverse
from django.utils import timezone


PROTECTED_MEDIA_ROOT = settings.PROTECTED_MEDIA_ROOT
protected_storage = FileSystemStorage(location=str(PROTECTED_MEDIA_ROOT))

# Create your models here.
class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    # stripe_product_id = 
    image = models.ImageField(blank=True, upload_to="products/", null=True)
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    handle = models.SlugField(unique=True)
    #are we selling anything more than a million?
    price = models.DecimalField(max_digits=10, decimal_places=2, default=9.99)
    org_price = models.DecimalField(max_digits=10, decimal_places=2, default=9.99)
    
    # stripe_price_id
    #maybe convert this to MVR for localisation purposes
    stripe_price = models.IntegerField(default=9.99) 
    #deafults to 9 but is / 12.45 for USD, * for MVR
    price_changed_timestamp = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)

    timestamp = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.price != self.org_price:
            self.org_price = self.price

            self.stripe_price = int(self.price / 15)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("products:detail", kwargs={"handle": self.handle})
    
    def get_manage_url(self):
        return reverse("products:manage", kwargs={"handle": self.handle})

def handle_product_attachement_upload(instance, filename):
    return f"products/{instance.product.handle}/attachments/{filename}" #or instance.handle


class ProductAttachment(models.Model):
    # item_id = 
    name = models.CharField(max_length=120)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    file = models.FileField(upload_to=handle_product_attachement_upload, storage = protected_storage)
    handle = models.SlugField(unique=True)
    is_downloadable = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=9.99)
    active = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.name:
            # stem, suffix
            self.name = pathlib.Path(self.file.name).name
        super().save(*args, **kwargs)
    
    @property
    def display_name(self):
        return self.name or pathlib.Path(self.file.name).name

    def get_download_url(self):
        return reverse("products:download", kwargs={"handle": self.product.handle, "pk": self.pk}) # or self.handle
    
