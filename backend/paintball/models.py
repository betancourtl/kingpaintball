from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Brand(TimeStampMixin):
    name = models.CharField(max_length=25, blank=True, default='', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Category(TimeStampMixin):
    name = models.CharField(max_length=25, blank=True, default='', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Condition(TimeStampMixin):
    name = models.CharField(max_length=25, blank=True, default='', unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Item(TimeStampMixin):
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

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['created_at']


class Image(TimeStampMixin):
    # fk's
    image = models.ImageField(
        upload_to='uploads', default='images/default.png')
    # the viewset can now add images to the fields array to get all the images
    # for an item.
    item = models.ForeignKey(
        Item,
        related_name="images",
        on_delete=models.CASCADE
    )


class Like(TimeStampMixin):
    item = models.ForeignKey(
        Item,
        related_name="likes",
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        related_name="likes",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.item

    class Meta:
        unique_together = (('item', 'user'),)
        ordering = ['item']


class Comment(TimeStampMixin):
    comment = models.TextField(blank=False)
    item = models.ForeignKey(
        Item, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.comment)[:50]

    class Meta:
        ordering = ['created_at']
