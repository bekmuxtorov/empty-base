from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
import math
from .models import (
    DataRecord, BKGazCurrentData, BKGazHourlyArchive, 
    BKGazDailyArchive, BKGazMonthlyArchive, BKGazEmergencyArchive, 
    BKGazVariableArchive
)
from .serializers import (
    DataRecordSerializer, BKGazCurrentDataSerializer, BKGazHourlyArchiveSerializer,
    BKGazDailyArchiveSerializer, BKGazMonthlyArchiveSerializer, 
    BKGazEmergencyArchiveSerializer, BKGazVariableArchiveSerializer
)

class DataRecordViewSet(viewsets.ModelViewSet):
    queryset = DataRecord.objects.all()
    serializer_class = DataRecordSerializer

class BKGazCurrentDataViewSet(viewsets.ModelViewSet):
    queryset = BKGazCurrentData.objects.all()
    serializer_class = BKGazCurrentDataSerializer

class BKGazHourlyArchiveViewSet(viewsets.ModelViewSet):
    queryset = BKGazHourlyArchive.objects.all()
    serializer_class = BKGazHourlyArchiveSerializer

class BKGazDailyArchiveViewSet(viewsets.ModelViewSet):
    queryset = BKGazDailyArchive.objects.all()
    serializer_class = BKGazDailyArchiveSerializer

class BKGazMonthlyArchiveViewSet(viewsets.ModelViewSet):
    queryset = BKGazMonthlyArchive.objects.all()
    serializer_class = BKGazMonthlyArchiveSerializer

class BKGazEmergencyArchiveViewSet(viewsets.ModelViewSet):
    queryset = BKGazEmergencyArchive.objects.all()
    serializer_class = BKGazEmergencyArchiveSerializer

class BKGazVariableArchiveViewSet(viewsets.ModelViewSet):
    queryset = BKGazVariableArchive.objects.all()
    serializer_class = BKGazVariableArchiveSerializer

def safe_float(val):
    if val is None:
        return None
    try:
        f = float(val)
        if math.isnan(f) or math.isinf(f) or abs(f) > 1e10:
            return None
        return f
    except (ValueError, TypeError):
        return None

class BKGazDataIngestView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        meta = data.get('meta', {})
        device_address = str(meta.get('device_address', 'unknown'))

        with transaction.atomic():
            # Process Current
            current_data = data.get('current')
            if current_data:
                BKGazCurrentData.objects.create(
                    device_address=device_address,
                    timestamp=current_data.get('timestamp'),
                    work_hours=safe_float(current_data.get('work_hours')),
                    work_volume=safe_float(current_data.get('work_volume')),
                    std_volume=safe_float(current_data.get('std_volume')),
                    pressure=safe_float(current_data.get('pressure')),
                    temperature=safe_float(current_data.get('temperature')),
                    correction_coef=safe_float(current_data.get('correction_coef')),
                    work_flow=safe_float(current_data.get('work_flow')),
                    std_flow=safe_float(current_data.get('std_flow')),
                    emergency_bits=current_data.get('emergency_bits'),
                    emergency_active=current_data.get('emergency_active', False),
                    emergency_codes=current_data.get('emergency_codes', [])
                )
            
            # Process Hourly
            hourly = data.get('hourly', {})
            hourly_records = hourly.get('records', [])
            for rec in hourly_records:
                BKGazHourlyArchive.objects.update_or_create(
                    device_address=device_address,
                    timestamp=rec.get('timestamp'),
                    defaults={
                        'pressure': safe_float(rec.get('pressure')),
                        'temperature': safe_float(rec.get('temperature')),
                        'acc_work_vol': safe_float(rec.get('acc_work_vol')),
                        'acc_std_vol': safe_float(rec.get('acc_std_vol')),
                    }
                )

            # Process Daily
            daily = data.get('daily', {})
            daily_records = daily.get('records', [])
            for rec in daily_records:
                BKGazDailyArchive.objects.update_or_create(
                    device_address=device_address,
                    timestamp=rec.get('timestamp'),
                    defaults={
                        'pressure': safe_float(rec.get('pressure')),
                        'temperature': safe_float(rec.get('temperature')),
                        'work_vol': safe_float(rec.get('work_vol')),
                        'std_vol': safe_float(rec.get('std_vol')),
                        'acc_work_vol': safe_float(rec.get('acc_work_vol')),
                        'acc_std_vol': safe_float(rec.get('acc_std_vol')),
                    }
                )

            # Process Monthly
            monthly = data.get('monthly', {})
            monthly_records = monthly.get('records', [])
            for rec in monthly_records:
                BKGazMonthlyArchive.objects.update_or_create(
                    device_address=device_address,
                    timestamp=rec.get('timestamp'),
                    defaults={
                        'work_vol': safe_float(rec.get('work_vol')),
                        'std_vol': safe_float(rec.get('std_vol')),
                        'acc_work_vol': safe_float(rec.get('acc_work_vol')),
                        'acc_std_vol': safe_float(rec.get('acc_std_vol')),
                    }
                )

            # Process Emergency
            emergency = data.get('emergency', {})
            emergency_records = emergency.get('records', [])
            for rec in emergency_records:
                BKGazEmergencyArchive.objects.create(
                    device_address=device_address,
                    timestamp=rec.get('timestamp'),
                    code_word=rec.get('code_word'),
                    changed=rec.get('changed', False),
                    value=safe_float(rec.get('value')),
                    errors=rec.get('errors', [])
                )

            # Process Variable
            variable = data.get('variable', {})
            variable_records = variable.get('records', [])
            for rec in variable_records:
                BKGazVariableArchive.objects.create(
                    device_address=device_address,
                    timestamp=rec.get('timestamp'),
                    n2_concentration=safe_float(rec.get('n2_concentration')),
                    co2_concentration=safe_float(rec.get('co2_concentration')),
                    gas_density=safe_float(rec.get('gas_density')),
                    baro_pressure=safe_float(rec.get('baro_pressure')),
                    p_lower_bound=safe_float(rec.get('p_lower_bound')),
                    p_upper_bound=safe_float(rec.get('p_upper_bound')),
                    temperature_sub=safe_float(rec.get('temperature_sub')),
                    max_flow=safe_float(rec.get('max_flow')),
                    min_flow=safe_float(rec.get('min_flow')),
                    min_flow_sub=safe_float(rec.get('min_flow_sub')),
                    max_flow_sub=safe_float(rec.get('max_flow_sub'))
                )

        return Response({"status": "success", "message": "Ma'lumotlar muvaffaqiyatli saqlandi."}, status=status.HTTP_201_CREATED)
