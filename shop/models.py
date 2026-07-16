from django.db import models

# Create your models here.
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
   name = models.CharField(max_length=100, unique=True)
   slug = models.SlugField(max_length=120, unique=True, blank=True)
   description = models.TextField(blank=True)
   image = models.ImageField(upload_to="categories/", blank=True, null=True)
   active = models.BooleanField(default=True)
   created_at = models.DateTimeField(auto_now_add=True)

   class Meta:
      ordering = ["name"]
      verbose_name_plural = "Categories"

   def __str__(self):
      return self.name

   def save(self, *args, **kwargs):
      if not self.slug:
         self.slug = slugify(self.name)
      super().save(*args, **kwargs)

   def get_absolute_url(self):
      return reverse(
         "category_detail",
         kwargs={
               "category_slug": self.slug,
         }
      )


class Home(models.Model):
   category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="homes")

   name = models.CharField(max_length=200)
   slug = models.SlugField(max_length=255, unique=True, blank=True)
   sku = models.CharField(max_length=100, unique=True)

   badge = models.CharField(max_length=100, blank=True)
   series = models.CharField(max_length=100, blank=True)

   short_description = models.TextField(blank=True)
   description = models.TextField()

   main_image = models.ImageField(upload_to="homes/")
   spec_sheet = models.FileField(upload_to="spec-sheets/", blank=True, null=True)

   price = models.DecimalField(max_digits=12, decimal_places=2)
   price_per_sqft = models.DecimalField(max_digits=10, decimal_places=2)

   square_feet = models.PositiveIntegerField()
   bedrooms = models.PositiveSmallIntegerField()
   bathrooms = models.PositiveSmallIntegerField()
   stories = models.PositiveSmallIntegerField(default=1)

   featured = models.BooleanField(default=False)
   active = models.BooleanField(default=True)

   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

   class Meta:
      ordering = ["name"]

   def __str__(self):
      return self.name

   def save(self, *args, **kwargs):
      creating = self.pk is None

      super().save(*args, **kwargs)

      if creating and not self.slug:
         self.slug = f"{slugify(self.name)}-{self.pk}"
         super().save(update_fields=["slug"])

   def get_absolute_url(self):
      return reverse(
         "home_detail",
         kwargs={
               "category_slug": self.category.slug,
               "slug": self.slug,
         }
      )


class HomeGallery(models.Model):
   home = models.ForeignKey(Home, on_delete=models.CASCADE, related_name="gallery")
   image = models.ImageField(upload_to="homes/gallery/")
   title = models.CharField(max_length=100, blank=True)
   display_order = models.PositiveIntegerField(default=0)

   class Meta:
      ordering = ["display_order", "id"]
      verbose_name = "Gallery Image"
      verbose_name_plural = "Gallery Images"

   def __str__(self):
      return self.title or f"{self.home.name} Image"


class Specification(models.Model):
   home = models.ForeignKey(Home, on_delete=models.CASCADE, related_name="specifications")
   title = models.CharField(max_length=150)
   value = models.CharField(max_length=255)
   display_order = models.PositiveIntegerField(default=0)

   class Meta:
      ordering = ["display_order", "id"]

   def __str__(self):
      return f"{self.title} - {self.home.name}"
   


class Order(models.Model):
   STATUS_CHOICES = (
      ("pending", "Pending"),
      ("contacted", "Contacted"),
      ("completed", "Completed"),
      ("cancelled", "Cancelled"),
   )

   home = models.ForeignKey(
      Home,
      on_delete=models.CASCADE,
      related_name="orders"
   )

   # Customer Information
   first_name = models.CharField(max_length=100)
   last_name = models.CharField(max_length=100)
   email = models.EmailField()
   phone = models.CharField(max_length=30)

   # Shipping Information
   country = models.CharField(max_length=100)
   city = models.CharField(max_length=100)
   address = models.TextField()

   # Additional Information
   notes = models.TextField(blank=True)

   status = models.CharField(
      max_length=20,
      choices=STATUS_CHOICES,
      default="pending"
   )

   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

   class Meta:
      ordering = ["-created_at"]

   def __str__(self):
      return f"{self.first_name} {self.last_name} - {self.home.name}"

   def get_absolute_url(self):
      return reverse(
         "order_detail",
         kwargs={
            "pk": self.pk,
         }
      )