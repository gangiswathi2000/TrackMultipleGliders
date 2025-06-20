from django.contrib import admin
from .models import Glider, ScientificData, ComputerData

@admin.register(Glider)
class GliderAdmin(admin.ModelAdmin):
    list_display = (
        'glider_id',
        'dateCreated',
        'source_file',
        'institution',
        'creator',
        'summary',
        'contributors',
        'startOfCoverage',
        'endOfCoverage'
    )
    search_fields = ('glider_id', 'operator')
@admin.register(ScientificData)
class ScientificDataAdmin(admin.ModelAdmin):
    list_display = ('glider', 'precise_time', 'latitude', 'longitude', 'depth', 'temperature', 'salinity', 'oxygen', 'cdom', 
                    'chlorophyll', 'density', 'precise_lat','precise_lon','precise_time')
    list_filter = ('glider', 'precise_time')
    search_fields = ('glider__glider_id','precise_time')



@admin.register(ComputerData)
class ComputerDataAdmin(admin.ModelAdmin):
    list_display = ('glider', 'pitch', 'roll', 'u', 'v')
    list_filter = ('glider', 'pitch')
    search_fields = ('glider__glider_id','pitch')
  