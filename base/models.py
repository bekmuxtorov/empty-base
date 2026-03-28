from django.db import models

class DataRecord(models.Model):
    device_id = models.CharField(max_length=100, verbose_name="Device ID")
    meter_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="Meter ID")
    phone = models.CharField(max_length=30, blank=True, null=True, verbose_name="Phone")
    
    pressure = models.FloatField(default=0, verbose_name="Pressure")
    temperature = models.FloatField(default=0, verbose_name="Temperature")
    volume = models.FloatField(default=0, verbose_name="Volume")
    
    signal = models.IntegerField(default=0, verbose_name="Signal")
    battery = models.FloatField(default=0, verbose_name="Battery")
    status = models.CharField(max_length=30, default="online", verbose_name="Status")
    
    timestamp = models.DateTimeField(verbose_name="Timestamp")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        verbose_name = "Data Record"
        verbose_name_plural = "Data Records"
        ordering = ['-timestamp']

    def __str__(self):
        return f"Device {self.device_id} - {self.timestamp}"
