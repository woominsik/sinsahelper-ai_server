from django.db import models

# Create your models here.

class Item(models.Model):
    item_id = models.BigIntegerField(primary_key=True)
    delivery_score = models.BigIntegerField(blank=True, null=True)
    item_url = models.CharField(max_length=255, blank=True, null=True)
    main_category = models.CharField(max_length=255, blank=True, null=True)
    photo = models.CharField(max_length=255, blank=True, null=True)
    price_today = models.CharField(max_length=255, blank=True, null=True)
    price_yesterday = models.CharField(max_length=255, blank=True, null=True)
    quality_score = models.BigIntegerField(blank=True, null=True)
    review = models.CharField(max_length=255, blank=True, null=True)
    size_score = models.BigIntegerField(blank=True, null=True)
    sub_category = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'item'