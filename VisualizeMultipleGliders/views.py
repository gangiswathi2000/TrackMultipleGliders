from django.shortcuts import render
import plotly.express as px
from VisualizeMultipleGliders.models import Glider, Glider_Research_Data
import pandas as pd
import numpy as np
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
def glider_map_view(request):
    return render(request, 'glider_map.html')
def remove_nan(obj):
    if isinstance(obj, float) and (np.isnan(obj) or np.isinf(obj)):
        return None
    if isinstance(obj, dict):
        return {k: remove_nan(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [remove_nan(x) for x in obj]
    return obj


def plot_glider_data(request):
    variables_units={'temperature': '°C', 'salinity': 'PSU', 'oxygen': 'ml/l', 'dep':'m'}
    colorscales_range={'temperature': [6,12]}
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            gliderID=data.get("glider_id")
            track = data.get("track", [])
            x_axis = data.get("x_axis")
            y_axis = data.get("y_axis")
            color=data.get("color")
            if not track:
                return JsonResponse({'plot_html': "<p>No data provided.</p>"})
            df = pd.DataFrame(track)
            start_time = str(df['startOfCoverage'].iloc[0])
            end_time = str(df['endOfCoverage'].iloc[0])
            id = gliderID.split("-")[0]
            title = f"{id}_{start_time.replace(':','').replace('-','').replace('T','')}-{end_time.replace(':','').replace('-','').replace('T','')}"
            y_unit = variables_units.get(y_axis)
            color_unit=variables_units.get(color)
            scale=colorscales_range.get(color)
            df['precise_time'] = pd.to_datetime(df['time'],format="ISO8601", utc=True)
            fig = px.scatter(
                df,
                x=x_axis,
                y=y_axis,  
                color=color,  
                color_continuous_scale='thermal',
                template='plotly_white',
                range_color=scale,
                title=title,
                hover_data=[x_axis,y_axis,color]
            )
            fig.update_layout(
            coloraxis_colorbar=dict(
                title=f"{color} ({color_unit})"
            ),
            xaxis_title=f"{x_axis}",
            yaxis_title=f"{y_axis}, ({y_unit})",
            title_x=0.5,
            title_font=dict(size=16)
            )
            fig.update_layout(width=1000)
            fig.update_yaxes(autorange='reversed')
            return JsonResponse({'plot_html': fig.to_html(full_html=False)})
        except Exception as e:
            return JsonResponse({'plot_html': f"<p>Error: {str(e)}</p>"})
def glider_data_to_display(request):
    data = list(
        Glider_Research_Data.objects
        .values('glider__glider_id','glider__startOfCoverage',
            'glider__endOfCoverage','precise_time', 'precise_lat', 'precise_lon', 'depth','temperature', 'oxygen','salinity')
    )
    cleaned_data = remove_nan(data)
    return JsonResponse(cleaned_data, safe=False)