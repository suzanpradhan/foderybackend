import re
from django.db.models.query import QuerySet
from django.shortcuts import render
from rest_framework import generics, serializers
from rest_framework.response import Response
from QuickOrder.serializers import QuickOrderSerializer
from Products.models import Item
from Products.serilaizers import QuickOrderCartItemSerializer, ItemSerializer
from QuickOrder.models import PeopleGroupType, Diet, FoodType
from QuickOrder.serializers import PeopleGroupTypeSerializer, DietSerializer, FoodTypeSerializer
from random import randint

class GetPeopleGroupType(generics.ListAPIView):
    serializer_class = PeopleGroupTypeSerializer

    def get(self, request):
        queryset = PeopleGroupType.objects.filter(status=True, numberOfPeople__gte = 1)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

class GetAllDiets(generics.ListAPIView):
    serializer_class = DietSerializer

    def get(self, request):
        queryset = Diet.objects.filter(status=True)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

class GetAllFoodTypes(generics.ListAPIView):
    serializer_class = FoodTypeSerializer

    def get(self, request):
        queryset = FoodType.objects.filter(status=True)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

class QuickOrder(generics.GenericAPIView):
    def post(self,request,*args, **kwargs):
        serializer = QuickOrderSerializer(data=request.data)
        if (serializer.is_valid()):
            validatedData = serializer.validated_data
            result = []
            allItems = None
            allItems = Item.objects.only("pk", "servings", "newPrice")
            if validatedData.get('food_types'):
                # for food_type in validatedData.get('food_types'):
                allItems = allItems.filter(foodTypes__in=validatedData.get('food_types'))
            dietsRequestData = validatedData.get('diets')
            if validatedData.get('diets'):
                for dietDict in dietsRequestData:
                    allItems = allItems.filter(diets__id=dietDict["diet"])

            if validatedData.get('groupId') == 1 and len(dietsRequestData) == 1:
                result = self.test(allItems, validatedData.get('budgetMax'), 1, result)
            else:
                totalPerson = 0
                for dietSyncPerson in dietsRequestData:
                    totalPerson = totalPerson + dietSyncPerson["people"]
                result = self.test2(allItems, validatedData.get('budgetMax'), totalPerson, result)
                # print("here") 
                # dietFilteredItems = allItems.filter(diets__id=dietsRequestData[0]["diet"])
                # usedPrice = 0
                # maxPrice=validatedData.get('budgetMax')
                # while True:
                #     resultData = self.getItemsWithQuantity(filteredItems=dietFilteredItems, maxPrice=maxPrice-usedPrice, maxPeople=1, result=result)
                #     print(resultData["usedPrice"])
                #     usedPrice = usedPrice + resultData["usedPrice"]
                #     if usedPrice < validatedData.get('budgetMax'):
                #         result = resultData["result"]
                #     else:
                #         result = resultData["result"]
                #         break
                
            # if validatedData.get('diets'):
            #     for dietDict in validatedData.get('diets'):
            #         allItems = allItems.filter(diets__id=dietDict["diet"])

                
            
            # if validatedData.get('groupId') == 1:
            #     if len(validatedData.get('diets')) < 1:
            #         allItems = allItems.filter(newPrice__range=(validatedData.get('budgetMin'), validatedData.get('budgetMax')))
            #         if allItems.exists():
            #             result = [{
            #                 "itemId" : allItems.first().id,
            #                 "quantity" : 1,
            #             }]
            #     else:
                    
            # else:
            #     totalPerson = 0
            #     for dietSyncPerson in validatedData.get('diets'):
            #         totalPerson = totalPerson + dietSyncPerson["people"]
            #     eachPersonMaxPrice = validatedData.get('budgetMax') / totalPerson
            #     for dietSyncPerson in validatedData.get('diets'):
            #         result = self.getItemsWithQuantity(filteredItems=allItems, maxPrice=eachPersonMaxPrice*dietSyncPerson["people"], maxPeople=dietSyncPerson["people"], result=result)
            return Response({'data':result})
        else:
            return Response(serializer.errors)
    
    def test(self, querySet, maxPrice, maxPeople, result):
        usedPrice = 0
        while True:
            itemsFilteredByMaxPrice = querySet.filter(newPrice__range=(0, maxPrice-usedPrice)).order_by('newPrice')
            if itemsFilteredByMaxPrice.exists():
                for i in range(maxPeople):
                    randomItem = itemsFilteredByMaxPrice[randint(0, len(itemsFilteredByMaxPrice) - 1)]
                    randomItemID = randomItem.id
                    prevItemIndex = None
                    for j in range(len(result)):
                        if (result[j]['itemId']==randomItemID):
                            prevItemIndex = j
                    if prevItemIndex != None:
                        result[prevItemIndex]['quantity'] = result[prevItemIndex]['quantity'] + 1
                        usedPrice = usedPrice + randomItem.newPrice
                    else:
                        result.append({
                            "itemId" : randomItemID,
                            "item":QuickOrderCartItemSerializer(randomItem).data,
                            "quantity" : 1,
                        })
                        usedPrice = usedPrice + randomItem.newPrice
            else:
                break
                    # usedPrice = usedPrice + randomItem.newPrice
        return result

    def test2(self, querySet, maxPrice, maxPeople, result):
        eachPersonMaxPrice = maxPrice / maxPeople
        usedPrice = 0
        totalDietSyncPrice = eachPersonMaxPrice * maxPeople
        while True:
            dietAllItems = querySet.filter(newPrice__range=(0, maxPrice-usedPrice)).order_by('newPrice')
            if dietAllItems.exists():
                gTotalPrice = 0
                gPeople = 0
                while True:
                    if gTotalPrice < totalDietSyncPrice and gPeople < maxPeople:
                        randomItem = dietAllItems[randint(0, len(dietAllItems) - 1)]
                        randomItemID = randomItem.id
                        prevItemIndex = None
                        for j in range(len(result)):
                            if (result[j]['itemId']==randomItemID):
                                prevItemIndex = j
                        if prevItemIndex != None:
                            result[prevItemIndex]['quantity'] = result[prevItemIndex]['quantity'] + 1
                            gTotalPrice = gTotalPrice + randomItem.newPrice
                            usedPrice = usedPrice + randomItem.newPrice
                            gPeople = gPeople + randomItem.servings
                        else:
                            result.append({
                                "itemId" : randomItemID,
                                "item":QuickOrderCartItemSerializer(randomItem).data,
                                "quantity" : 1,
                            })
                            gTotalPrice = gTotalPrice + randomItem.newPrice
                            usedPrice = usedPrice + randomItem.newPrice
                            gPeople = gPeople + randomItem.servings
                    else:
                        break
            else:
                break
        return result

                
            # usedPrice = usedPrice + resultData["usedPrice"]
            # if usedPrice < validatedData.get('budgetMax'):
            #     result = resultData["result"]
            # else:
            #     result = resultData["result"]
            #     break
    
    def getItemsWithQuantity(self, filteredItems, maxPrice:float, maxPeople:int, result:list):
        eachPersonMaxPrice = maxPrice / maxPeople
        usedPrice = 0
        dietAllItems = filteredItems.filter(newPrice__range=(0, eachPersonMaxPrice)).order_by('newPrice')
        if dietAllItems.exists():
            if len(dietAllItems) == 1:
                result.append({
                    "itemId" : dietAllItems.first().id,
                    "quantity" : maxPeople,
                })
                usedPrice = usedPrice + dietAllItems.first().newPrice
            else:
                for i in range(maxPeople):
                    randomItem = dietAllItems[randint(0, len(dietAllItems) - 1)]
                    randomItemID = dietAllItems[randint(0, len(dietAllItems) - 1)].id
                    prevItemIndex = None
                    for j in range(len(result)):
                        if (result[j]['itemId']==randomItemID):
                            prevItemIndex = j
                    if prevItemIndex != None:
                        result[prevItemIndex]['quantity'] = result[prevItemIndex]['quantity'] + 1
                        usedPrice = usedPrice + randomItem.newPrice
                    else:
                        result.append({
                            "itemId" : randomItemID,
                            "quantity" : 1,
                        })
                        usedPrice = usedPrice + randomItem.newPrice
                        
        else:
            totalDietSyncPrice = eachPersonMaxPrice * maxPeople
            dietAllItems = filteredItems.filter(newPrice__range=(eachPersonMaxPrice, totalDietSyncPrice)).order_by('newPrice')
            if dietAllItems.exists():
                gTotalPrice = 0
                gPeople = 0
                while True:
                    if gTotalPrice < totalDietSyncPrice and gPeople < maxPeople:
                        randomItem = dietAllItems[randint(0, len(dietAllItems) - 1)]
                        randomItemID = randomItem.id
                        prevItemIndex = None
                        for j in range(len(result)):
                            if (result[j]['itemId']==randomItemID):
                                prevItemIndex = j
                        if prevItemIndex != None:
                            result[prevItemIndex]['quantity'] = result[prevItemIndex]['quantity'] + 1
                            gTotalPrice = gTotalPrice + randomItem.newPrice
                            gPeople = gPeople + randomItem.servings
                        else:
                            result.append({
                                "itemId" : randomItemID,
                                "quantity" : 1,
                            })
                            gTotalPrice = gTotalPrice + randomItem.newPrice
                            gPeople = gPeople + randomItem.servings
                    else:
                        break
        return {
            "usedPrice": usedPrice,
            "result":result
            }
