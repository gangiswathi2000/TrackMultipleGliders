from django.shortcuts import render
import plotly.express as px
from VisualizeMultipleGliders.models import ScientificData,Glider,ComputerData
import pandas as pd
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
def glider_map_view(request):
    return render(request, 'glider_map.html')
@csrf_exempt
def plot_glider_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            track = data.get("track", [])
            if not track:
                return JsonResponse({'plot_html': "<p>No data provided.</p>"})
            df = pd.DataFrame(track)
            df['precise_time'] = pd.to_datetime(df['time'],format="ISO8601", utc=True)
            fig = px.scatter(
                df,
                x="lon",
                y="dep",  
                color="time",  
                title="Glider Positions Over Time",
                hover_data=["lat", "lon"]
            )
            fig.update_layout(height=600)
            return JsonResponse({'plot_html': fig.to_html(full_html=False)})

        except Exception as e:
            return JsonResponse({'plot_html': f"<p>Error: {str(e)}</p>"})
def glider_data_to_display(request):
    data = list(
        ScientificData.objects
        .values('glider__glider_id','precise_time', 'precise_lat', 'precise_lon', 'depth')
    )
    return JsonResponse(data, safe=False)
    