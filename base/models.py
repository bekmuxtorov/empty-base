from django.db import models

class DataRecord(models.Model):
    field1 = models.CharField(max_length=255, verbose_name="Field 1", null=True, blank=True)
    field2 = models.CharField(max_length=255, verbose_name="Field 2", null=True, blank=True)
    field3 = models.CharField(max_length=255, verbose_name="Field 3", null=True, blank=True)
    field4 = models.CharField(max_length=255, verbose_name="Field 4", null=True, blank=True)
    field5 = models.CharField(max_length=255, verbose_name="Field 5", null=True, blank=True)

    class Meta:
        verbose_name = "Data Record"
        verbose_name_plural = "Data Records"

    def __str__(self):
        return f"Record {self.id}: {self.field1}"
