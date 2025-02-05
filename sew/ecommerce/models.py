from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Master(models.Model):
    name = models.CharField(max_length=100)  # Compulsory field
    img = models.ImageField(upload_to='images/', blank=True, null=True)  # Optional field for image
    category = models.CharField(max_length=50, blank=True, null=True)  # Optional field for category
    description = models.TextField(blank=True, null=True)  # Optional field for description

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, related_name='categories_created', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active')

    def __str__(self):
        return self.name    


class Offer(models.Model):
    title1 = models.CharField(max_length=255)  # Primary title of the offer
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='offer/')  # Optional subtitle
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price with up to 2 decimal places
    title2 = models.CharField(max_length=255, blank=True, null=True)  # Optional secondary title
    description = models.TextField(blank=True, null=True)  # Optional detailed description
    day_of_offer = models.IntegerField()  # Date of the offer
    is_active = models.BooleanField(default=True)  # Indicates if the offer is active
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when the offer is created
    modified_at = models.DateTimeField(auto_now=True)  # Automatically update when the offer is modified
    created_by = models.ForeignKey(User, related_name='offers_created', on_delete=models.SET_NULL, null=True)  # User who created the offer
    modified_by = models.ForeignKey(User, related_name='offers_modified', on_delete=models.SET_NULL, null=True)  # User who last modified the offer

    def __str__(self):
        return f"{self.title1} - {self.subtitle or 'No Subtitle'}"

    def save(self, *args, **kwargs):
        # Automatically set the 'created_by' and 'modified_by' fields if they are not already set
        if not self.created_by:
            self.created_by = kwargs.get('user')  # The user should be passed as a keyword argument when saving
        self.modified_by = kwargs.get('user')  # The user should be passed as a keyword argument when saving
        super(Offer, self).save(*args, **kwargs)



class Product(models.Model):
    RATING_CHOICES = [
        (0, '0'),  # Set default value to 0
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products/')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    stock = models.IntegerField(default=0)
    brand_name = models.CharField(max_length=255, blank=True)
    featured = models.BooleanField(default=False)
    rating = models.IntegerField(choices=RATING_CHOICES, default=0)
    no_of_people = models.PositiveIntegerField(default=0)

    created_by = models.ForeignKey(User, related_name='products_created', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, related_name='products_updated', on_delete=models.SET_NULL, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/product/{self.id}/"

    def clean(self):
        if self.featured:
            # Count the number of featured products excluding the current one (if updating)
            existing_featured = Product.objects.filter(featured=True).exclude(id=self.id).count()
            if existing_featured >= 4:
                raise ValidationError("Sirf 4 products ko feature kiya ja sakta hai.")
    
    def save(self, *args, **kwargs):
        self.clean()  # Validate before saving
        super().save(*args, **kwargs)


class Testimonial(models.Model):
    name = models.CharField(max_length=255)
    profession = models.CharField(max_length=255)
    image = models.ImageField(upload_to='testimonials/')
    feedback = models.TextField()
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.is_active:
            active_count = Testimonial.objects.filter(is_active=True).count()
            if active_count >= 5 and not self.pk:  # Ensure only new ones are restricted
                raise ValidationError("Only 5 testimonials can be active at a time.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveIntegerField(choices=[(i, f"{i} Star") for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.product.name} by {self.rating} stars"
    


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)  # To track when the user subscribed

    def __str__(self):
        return self.email

