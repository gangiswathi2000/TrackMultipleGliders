from django.db import models

class Glider(models.Model):
    glider_id = models.CharField(max_length=100, unique=True)
    dateCreated = models.DateTimeField(null=True, blank=True)
    source_file = models.CharField(max_length=255, null=True, blank=True)
    institution=models.CharField(max_length=255, null=True, blank=True)
    creator=models.CharField(max_length=255, null=True, blank=True)
    contributors=models.CharField(max_length=255, null=True, blank=True)
    startOfCoverage=models.DateTimeField(null=True, blank=True)
    endOfCoverage=models.DateTimeField(null=True, blank=True)
    summary= models.CharField(max_length=1000, null=True, blank=True)
    
    def __str__(self):
        return self.glider_id


class ScientificData(models.Model):
    glider = models.ForeignKey(Glider, on_delete=models.CASCADE, related_name='scientific_data')
    latitude = models.FloatField()
    longitude = models.FloatField()
    depth = models.FloatField()
    temperature = models.FloatField(null=True, blank=True)
    salinity = models.FloatField(null=True, blank=True)
    oxygen = models.FloatField(null=True, blank=True)
    cdom = models.FloatField(null=True, blank=True)
    chlorophyll = models.FloatField(null=True, blank=True)
    density = models.FloatField(null=True, blank=True)
    precise_lat = models.FloatField(null=True, blank=True)
    precise_lon = models.FloatField(null=True, blank=True)
    precise_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.glider.glider_id} | {self.precise_time}"

class ComputerData(models.Model):
    glider = models.ForeignKey(Glider, on_delete=models.CASCADE, related_name='computer_data')
    pitch = models.FloatField(null=True, blank=True)
    roll = models.FloatField(null=True, blank=True)
    u = models.FloatField(null=True, blank=True)
    v = models.FloatField(null=True, blank=True)
   
    def __str__(self):
        return f"{self.glider.glider_id} | {self.pitch} (Computer Data)"