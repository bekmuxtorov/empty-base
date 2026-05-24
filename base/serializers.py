from rest_framework import serializers
from .models import (
    DataRecord, BKGazCurrentData, BKGazHourlyArchive, 
    BKGazDailyArchive, BKGazMonthlyArchive, BKGazEmergencyArchive, 
    BKGazVariableArchive
)

class DataRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataRecord
        fields = '__all__'

class BKGazCurrentDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = BKGazCurrentData
        fields = '__all__'

class BKGazHourlyArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = BKGazHourlyArchive
        fields = '__all__'

class BKGazDailyArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = BKGazDailyArchive
        fields = '__all__'

class BKGazMonthlyArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = BKGazMonthlyArchive
        fields = '__all__'

class BKGazEmergencyArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = BKGazEmergencyArchive
        fields = '__all__'

class BKGazVariableArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = BKGazVariableArchive
        fields = '__all__'
