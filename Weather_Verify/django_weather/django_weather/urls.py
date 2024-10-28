
from django.contrib import admin 
from django.urls import path, include
from weather import tests as url_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(url_path))

]
