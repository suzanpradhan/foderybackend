from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views
urlpatterns = [
    # path('all/',views.GetDelete.as_view(),name='order-all'),
    # path('all/<int:id>/',views.GetDelete.as_view(),name='order-delete'),
    # path('<int:id>/',views.UpdateCreate.as_view(),name='order-update'),
    path('',views.UpdateCreate.as_view(),name='collection-add'),
]