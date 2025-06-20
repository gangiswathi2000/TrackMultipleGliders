from django.urls import path
from .views import glider_map_view, plot_glider_data, glider_data_to_display

urlpatterns = [
     path('', glider_map_view, name='glider_map'),
     path('plots/', plot_glider_data, name='plots'),
     path('gliderdata/',glider_data_to_display, name='glider_data_to_display')
]