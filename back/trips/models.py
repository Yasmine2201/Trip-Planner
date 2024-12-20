from django.db import models


class Trip(models.Model):
    trip_id = models.AutoField(primary_key=True)
    trip_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    latitude = models.FloatField()
    longitude = models.FloatField()


    def __str__(self):
        return f"Trip(id={self.trip_id}, name={self.trip_name}, start_date={self.start_date}, end_date={self.end_date}, latitude={self.latitude}, longitude={self.longitude})"