from django.core.management.base import BaseCommand
from VisualizeMultipleGliders.models import Glider, ScientificData, ComputerData
import xarray as xr
import pandas as pd
import os
from datetime import datetime

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('files', nargs='+', type=str)

    def handle(self, *args, **options):
        for file_path in options['files']:
            self.stdout.write(self.style.NOTICE(f"Reading file: {file_path}"))

            if not os.path.exists(file_path):
                self.stdout.write(self.style.ERROR(f" File not found: {file_path}"))
                continue

            ds = xr.open_dataset(file_path)
            glider_type= ds.attrs['platform_type']
           
            glider_id = ds.attrs.get("id")
            dateCreated = ds.attrs.get("date_created")
            summary= ds.attrs.get("summary")
            creator=ds.attrs.get("creator_name")
            contributors=ds.attrs.get("contributor_name")
            startOfCoverage=ds.attrs.get("time_coverage_start")
            endOfCoverage=ds.attrs.get("time_coverage_end")
            institution = ds.attrs.get("institution")
            source_file = os.path.basename(file_path)

            glider_obj, _ = Glider.objects.get_or_create(
                glider_id=glider_id,
                defaults={
                    "dateCreated": dateCreated,
                    "institution": institution,
                    "source_file": source_file,
                    "summary":summary,
                    "creator":creator,
                    "contributors":contributors,
                    "startOfCoverage":startOfCoverage,
                    "endOfCoverage":endOfCoverage,                    
                }
            )
            if  glider_type=='Slocum Glider' and 'dissolved_oxygen' in ds:
                oxygen_data=ds['dissolved_oxygen'].values
            elif glider_type=='Seaglider' and 'oxygen' in ds:
                oxygen_data=ds['oxygen'].values
            else:
                oxygen_data=None
            df = pd.DataFrame({
                "latitude": ds['latitude'].values,
                "longitude": ds['longitude'].values,
                "depth": ds['depth'].values,
                "temperature": ds['temperature'].values if 'temperature' in ds else None,
                "salinity": ds['salinity'].values if 'salinity' in ds else None,
                "oxygen": oxygen_data,
                "cdom": ds['CDOM'].values if 'CDOM' in ds else None,
                "chlorophyll": ds['chlorophyll'].values if 'chlorophyll' in ds else None,
                "density": ds['density'].values if 'density' in ds else None,
                "pitch": ds['pitch'].values if 'pitch' in ds else None,
                "roll": ds['roll'].values if 'roll' in ds else None,
                "u": ds['u'].values if 'u' in ds else None,
                "v": ds['v'].values if 'v' in ds else None,
                "precise_lat": ds['precise_lat'].values if 'precise_lat' in ds else None,
                "precise_lon": ds['precise_lon'].values if 'precise_lon' in ds else None,
                "precise_time": pd.to_datetime(ds['precise_time'].values).tz_localize("UTC") if 'precise_time' in ds else None,
            })

            self.stdout.write(self.style.NOTICE(f"Inserting {len(df)} rows..."))

            for _, row in df.iterrows():
                ScientificData.objects.create(
                    glider=glider_obj,
                    latitude=row.latitude,
                    longitude=row.longitude,
                    depth=row.depth,
                    temperature=row.temperature,
                    salinity=row.salinity,
                    oxygen=row.oxygen,
                    cdom=row.cdom,
                    chlorophyll=row.chlorophyll,
                    density=row.density,
                    precise_lat=row.precise_lat,
                    precise_lon=row.precise_lon,
                    precise_time=row.precise_time
                )
                ComputerData.objects.create(
                    glider=glider_obj,
                    pitch=row.pitch,
                    roll=row.roll,
                    u=row.u,
                    v=row.v
                )

            self.stdout.write(self.style.SUCCESS(f"Successfully imported {file_path}"))