from rest_framework import serializers
from .models import Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('item_id', 'item_url', 'main_category', 'sub_category','photo','review','price_today','price_yesterday','delivery_score','quality_score','size_score')