from rest_framework import serializers
from django.db import transaction
from .models import (
    DataRecord, BKGazCurrentData, BKGazHourlyArchive, 
    BKGazDailyArchive, BKGazMonthlyArchive, BKGazEmergencyArchive, 
    BKGazVariableArchive, RawArchiveBatch, RawPacketDetail
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


class RawPacketDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawPacketDetail
        fields = ['id', 'sequence_number', 'packet_hex', 'created_at']


class RawArchiveBatchSerializer(serializers.ModelSerializer):
    raw_packets = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=True
    )
    packets = RawPacketDetailSerializer(many=True, read_only=True)

    class Meta:
        model = RawArchiveBatch
        fields = [
            'id', 'device_id', 'meter_id', 'archive_type', 
            'start_address', 'end_address', 'packet_count', 
            'raw_packets', 'packets', 'created_at'
        ]

    def validate(self, attrs):
        raw_packets = attrs.get('raw_packets', [])
        packet_count = attrs.get('packet_count')
        if len(raw_packets) != packet_count:
            raise serializers.ValidationError(
                {"packet_count": f"Paketlar soni ({len(raw_packets)}) packet_count ({packet_count}) ga mos kelmaydi."}
            )
        return attrs

    def create(self, validated_data):
        raw_packets = validated_data.pop('raw_packets')
        with transaction.atomic():
            batch = RawArchiveBatch.objects.create(**validated_data)
            packets_to_create = []
            for index, packet in enumerate(raw_packets, start=1):
                packets_to_create.append(
                    RawPacketDetail(
                        batch=batch,
                        sequence_number=index,
                        packet_hex=packet
                    )
                )
            RawPacketDetail.objects.bulk_create(packets_to_create)
        return batch
