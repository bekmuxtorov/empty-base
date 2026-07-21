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
    
    archive_type = models.CharField(max_length=50, blank=True, null=True, verbose_name="Archive Type")
    raw_hex = models.TextField(blank=True, null=True, verbose_name="Raw Hex")
    message = models.TextField(blank=True, null=True, verbose_name="Message")
    
    timestamp = models.DateTimeField(null=True, blank=True, verbose_name="Timestamp")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        verbose_name = "Data Record"
        verbose_name_plural = "Data Records"
        ordering = ['-timestamp']

    def __str__(self):
        return f"Device {self.device_id} - {self.timestamp if self.timestamp else 'No Timestamp'}"

class BKGazCurrentData(models.Model):
    device_address = models.CharField(max_length=50, verbose_name="Qurilma manzili")
    timestamp = models.DateTimeField(verbose_name="Vaqt")
    work_hours = models.FloatField(null=True, blank=True, verbose_name="Ish soatlari")
    work_volume = models.FloatField(null=True, blank=True, verbose_name="Ishchi hajm (m³)")
    std_volume = models.FloatField(null=True, blank=True, verbose_name="Keltirilgan hajm (m³)")
    pressure = models.FloatField(null=True, blank=True, verbose_name="Bosim")
    temperature = models.FloatField(null=True, blank=True, verbose_name="Harorat")
    correction_coef = models.FloatField(null=True, blank=True, verbose_name="Korreksiya koeffitsienti")
    work_flow = models.FloatField(null=True, blank=True, verbose_name="Ishchi sarf (m³/s)")
    std_flow = models.FloatField(null=True, blank=True, verbose_name="Keltirilgan sarf (m³/s)")
    emergency_bits = models.IntegerField(null=True, blank=True, verbose_name="Xatolik bitlari")
    emergency_active = models.BooleanField(default=False, verbose_name="Xatolik faolmi")
    emergency_codes = models.JSONField(default=list, blank=True, verbose_name="Xatolik kodlari")
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Joriy Ko'rsatkich"
        verbose_name_plural = "1. Joriy Ko'rsatkichlar (Current)"
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.device_address} - {self.timestamp}"


class BKGazHourlyArchive(models.Model):
    device_address = models.CharField(max_length=50, verbose_name="Qurilma manzili")
    timestamp = models.DateTimeField(verbose_name="Vaqt")
    pressure = models.FloatField(null=True, blank=True, verbose_name="Bosim")
    temperature = models.FloatField(null=True, blank=True, verbose_name="Harorat")
    acc_work_vol = models.FloatField(null=True, blank=True, verbose_name="To'plangan ishchi hajm")
    acc_std_vol = models.FloatField(null=True, blank=True, verbose_name="To'plangan keltirilgan hajm")
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Soatlik Arxiv"
        verbose_name_plural = "2. Soatlik Arxivlar"
        ordering = ['-timestamp']
        unique_together = ('device_address', 'timestamp')

    def __str__(self):
        return f"{self.device_address} - {self.timestamp}"


class BKGazDailyArchive(models.Model):
    device_address = models.CharField(max_length=50, verbose_name="Qurilma manzili")
    timestamp = models.DateTimeField(verbose_name="Vaqt")
    pressure = models.FloatField(null=True, blank=True, verbose_name="Bosim")
    temperature = models.FloatField(null=True, blank=True, verbose_name="Harorat")
    work_vol = models.FloatField(null=True, blank=True, verbose_name="Ishchi hajm (sutka)")
    std_vol = models.FloatField(null=True, blank=True, verbose_name="Keltirilgan hajm (sutka)")
    acc_work_vol = models.FloatField(null=True, blank=True, verbose_name="Jami to'plangan ishchi hajm")
    acc_std_vol = models.FloatField(null=True, blank=True, verbose_name="Jami to'plangan keltirilgan hajm")
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Kunlik Arxiv"
        verbose_name_plural = "3. Kunlik Arxivlar"
        ordering = ['-timestamp']
        unique_together = ('device_address', 'timestamp')

    def __str__(self):
        return f"{self.device_address} - {self.timestamp.date() if self.timestamp else ''}"


class BKGazMonthlyArchive(models.Model):
    device_address = models.CharField(max_length=50, verbose_name="Qurilma manzili")
    timestamp = models.DateTimeField(verbose_name="Vaqt")
    work_vol = models.FloatField(null=True, blank=True, verbose_name="Ishchi hajm (oylik)")
    std_vol = models.FloatField(null=True, blank=True, verbose_name="Keltirilgan hajm (oylik)")
    acc_work_vol = models.FloatField(null=True, blank=True, verbose_name="Jami to'plangan ishchi hajm")
    acc_std_vol = models.FloatField(null=True, blank=True, verbose_name="Jami to'plangan keltirilgan hajm")
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Oylik Arxiv"
        verbose_name_plural = "4. Oylik Arxivlar"
        ordering = ['-timestamp']
        unique_together = ('device_address', 'timestamp')

    def __str__(self):
        return f"{self.device_address} - {self.timestamp.strftime('%Y-%m') if self.timestamp else ''}"


class BKGazEmergencyArchive(models.Model):
    device_address = models.CharField(max_length=50, verbose_name="Qurilma manzili")
    timestamp = models.CharField(max_length=50, null=True, blank=True, verbose_name="Vaqt") # --MM-DDTHH:MM:00 can be string since year is missing
    code_word = models.IntegerField(null=True, blank=True, verbose_name="Xatolik kodi (raqam)")
    changed = models.BooleanField(default=False, verbose_name="O'zgarganmi")
    value = models.FloatField(null=True, blank=True, verbose_name="Qiymat")
    errors = models.JSONField(default=list, blank=True, verbose_name="Xatolik turlari")
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Favqulodda Arxiv"
        verbose_name_plural = "5. Favqulodda Arxivlar"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.device_address} - {self.timestamp} - {self.code_word}"


class BKGazVariableArchive(models.Model):
    device_address = models.CharField(max_length=50, verbose_name="Qurilma manzili")
    timestamp = models.DateTimeField(verbose_name="Vaqt")
    n2_concentration = models.FloatField(null=True, blank=True, verbose_name="N2 konsentratsiyasi")
    co2_concentration = models.FloatField(null=True, blank=True, verbose_name="CO2 konsentratsiyasi")
    gas_density = models.FloatField(null=True, blank=True, verbose_name="Gaz zichligi")
    baro_pressure = models.FloatField(null=True, blank=True, verbose_name="Barometrik bosim")
    p_lower_bound = models.FloatField(null=True, blank=True, verbose_name="Bosim quyi chegarasi")
    p_upper_bound = models.FloatField(null=True, blank=True, verbose_name="Bosim yuqori chegarasi")
    temperature_sub = models.FloatField(null=True, blank=True, verbose_name="Almashtirish harorati")
    max_flow = models.FloatField(null=True, blank=True, verbose_name="Maks. sarf")
    min_flow = models.FloatField(null=True, blank=True, verbose_name="Min. sarf")
    min_flow_sub = models.FloatField(null=True, blank=True, verbose_name="Min. sarf alm.")
    max_flow_sub = models.FloatField(null=True, blank=True, verbose_name="Maks. sarf alm.")
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "O'zgaruvchilar Arxivi"
        verbose_name_plural = "6. O'zgaruvchilar (Settings)"
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.device_address} - {self.timestamp}"


class RawArchiveBatch(models.Model):
    device_id = models.CharField(max_length=100, verbose_name="Qurilma ID")
    meter_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="Hisoblagich ID")
    archive_type = models.CharField(max_length=50, blank=True, null=True, verbose_name="Arxiv turi")
    start_address = models.CharField(max_length=50, blank=True, null=True, verbose_name="Boshlang'ich manzil")
    end_address = models.CharField(max_length=50, blank=True, null=True, verbose_name="Yakuniy manzil")
    packet_count = models.IntegerField(verbose_name="Paketlar soni")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")

    class Meta:
        verbose_name = "Xom Paket To'plami"
        verbose_name_plural = "Xom Paket To'plamlari"
        ordering = ['-created_at']

    def __str__(self):
        return f"Batch {self.id} (Device: {self.device_id}, Meter: {self.meter_id})"


class RawPacketDetail(models.Model):
    batch = models.ForeignKey(RawArchiveBatch, on_delete=models.CASCADE, related_name='packets', verbose_name="To'plam")
    sequence_number = models.IntegerField(verbose_name="Tartib raqami")
    packet_hex = models.TextField(verbose_name="Xom paket (Hex)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")

    class Meta:
        verbose_name = "Xom Paket"
        verbose_name_plural = "Xom Paketlar"
        ordering = ['batch', 'sequence_number']
        unique_together = ('batch', 'sequence_number')

    def __str__(self):
        return f"Batch {self.batch_id} - Packet #{self.sequence_number}"

