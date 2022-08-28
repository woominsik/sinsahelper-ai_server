from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Item
from .serializers import ItemSerializer
from .ai_model import reference_by_url
import random

# Create your views here.
@api_view(['GET'])
def helloAPI(request):
    print(request)
    print("받았어요!")
    return Response("Hello API!")

@api_view(['GET'])
def item_view(request):
    item = Item.objects.get(item_id=45)
    item.delivery_score = 13
    item.save()
    serializer=ItemSerializer(item)
    return Response(serializer.data)

@api_view(['GET'])
def connect2(request):
    key = request.GET.get('key',None)

    return Response("OK")

@api_view(['GET'])
def crawl(request):
    key = request.GET.get('url',None)
    return Response(key)

@api_view(['GET'])
def connect(request):
    # print(request)
    key = request.GET.get('item_id',None)
    if(key==None):
        items = Item.objects.all()
        print(items)
        for item in items:
            print(item.item_url)
            # item_url을 ai모델에 넘겨주고 score값 저장
            scores = reference_by_url(item.item_url)
            update(scores,item.item_url)
        
        # update(scores,"https://store.musinsa.com/app/goods/947067")  #ai 모델 돌린 후 리턴 값 update로 넘겨줌
    else:
        print("key는 "+key)
        item = Item.objects.get(item_id=key)
        scores=reference_by_url(item.item_url)
        update(scores,item.item_url)

    return Response("OK")

def update(scores,url):
    item = Item.objects.get(item_url=url)
    item.delivery_score = scores[0]
    item.quality_score = scores[1]
    item.size_score = scores[2]
    item.save()

