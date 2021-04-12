from django.urls import path

from pix.views import index

urlpatterns = [path("<int:pk>/", index, name="index")]