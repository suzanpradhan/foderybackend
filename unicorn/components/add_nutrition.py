from django.http import request
from django.http.response import HttpResponseBadRequest
from django_unicorn.components import UnicornView

from Products.models import Nutrition


class AddNutritionView(UnicornView):
    uni_nutrition="askkf"

    def add(self):
        title=self.title
        quantity=self.quantity

        if title is None or quantity is None:
            return HttpResponseBadRequest("Title and Quantity both are required.")
        
        nurtrition_obj=Nutrition.objects.create(title=title,quantity=quantity)
        self.uni_nutrition.append(nurtrition_obj)


