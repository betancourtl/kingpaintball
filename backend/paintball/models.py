import datetime
from django.db import models
from django.contrib.auth.models import User

# tested model
# tested api
class Brand(models.Model):
    name = models.CharField(max_length=25, blank=True, default='', unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

# tested model
# tested api
class Category(models.Model):
    name = models.CharField(max_length=25, blank=True, default='', unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

# tested model
# tested api
class Condition(models.Model):
    name = models.CharField(max_length=25, blank=True, default='', unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

# tested model
# tested api
class Item(models.Model):
    title = models.CharField(max_length=255, blank=True, default='')
    sold = models.BooleanField(default=False)
    description = models.TextField(blank=True, default='')
    year = models.PositiveSmallIntegerField(blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    # Foreign Keys
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    condition = models.ForeignKey(Condition, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['created_at']

# tested model
class Image(models.Model):
    # fk's
    image = models.ImageField(upload_to='images', default='images/default.png')
    # the viewset can now add images to the fields array to get all the images
    # for an item.
    item = models.ForeignKey(Item, related_name="images",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# tested model
class Like(models.Model):
    item = models.ForeignKey(Item, related_name="likes", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="likes", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.item

    class Meta:
        unique_together = (('item', 'user'),)
        ordering = ['item']

# tested model
class Comment(models.Model):
    comment = models.TextField(blank=False)
    item = models.ForeignKey(Item, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.comment)[:50]

    class Meta:
        ordering = ['created_at']
