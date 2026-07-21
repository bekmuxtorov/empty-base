from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import DataRecord, RawArchiveBatch, RawPacketDetail
from django.utils import timezone

class DataRecordAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('datarecord-list')
        self.sample_data = {
            "device_id": "TEST-DEV-001",
            "meter_id": "TEST-MTR-123",
            "phone": "+998901234567",
            "pressure": 1.5,
            "temperature": 25.0,
            "volume": 105.0,
            "signal": 100,
            "battery": 99.0,
            "status": "online",
            "timestamp": timezone.now().isoformat()
        }

    def test_create_record(self):
        response = self.client.post(self.url, self.sample_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DataRecord.objects.count(), 1)
        self.assertEqual(DataRecord.objects.get().device_id, 'TEST-DEV-001')

    def test_get_records(self):
        DataRecord.objects.create(**self.sample_data)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_record(self):
        record = DataRecord.objects.create(**self.sample_data)
        update_url = reverse('datarecord-detail', args=[record.id])
        update_data = {"status": "offline"}
        response = self.client.patch(update_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        record.refresh_from_db()
        self.assertEqual(record.status, "offline")

    def test_delete_record(self):
        record = DataRecord.objects.create(**self.sample_data)
        delete_url = reverse('datarecord-detail', args=[record.id])
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(DataRecord.objects.count(), 0)

    def test_create_no_response_record(self):
        no_response_payload = {
            "device_id": "DEV-002",
            "meter_id": "MTR-5555",
            "phone": "+998901644101",
            "archive_type": "daily",
            "raw_hex": "",
            "status": "meter_no_response",
            "message": "Schotchik javob bermadi"
        }
        response = self.client.post(self.url, no_response_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DataRecord.objects.count(), 1)
        record = DataRecord.objects.get()
        self.assertEqual(record.device_id, "DEV-002")
        self.assertEqual(record.status, "meter_no_response")
        self.assertEqual(record.message, "Schotchik javob bermadi")
        self.assertEqual(record.archive_type, "daily")
        self.assertEqual(record.raw_hex, "")
        self.assertIsNone(record.timestamp)


class RawArchiveBatchAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('raw-packets-list')
        self.sample_payload = {
            "device_id": "DEV-002",
            "meter_id": "MTR-5555",
            "archive_type": "monthly",
            "start_address": "6086",
            "end_address": "6279",
            "raw_packets": [
                "%1600000816000000002D",
                "%16000000000495F02957",
                "%1604936D94000008175D"
            ],
            "packet_count": 3
        }

    def test_create_raw_archive_batch_success(self):
        response = self.client.post(self.url, self.sample_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RawArchiveBatch.objects.count(), 1)
        self.assertEqual(RawPacketDetail.objects.count(), 3)
        
        batch = RawArchiveBatch.objects.first()
        self.assertEqual(batch.device_id, "DEV-002")
        self.assertEqual(batch.meter_id, "MTR-5555")
        self.assertEqual(batch.archive_type, "monthly")
        self.assertEqual(batch.start_address, "6086")
        self.assertEqual(batch.end_address, "6279")
        self.assertEqual(batch.packet_count, 3)

        packets = list(batch.packets.all().order_by('sequence_number'))
        self.assertEqual(packets[0].packet_hex, "%1600000816000000002D")
        self.assertEqual(packets[0].sequence_number, 1)
        self.assertEqual(packets[1].packet_hex, "%16000000000495F02957")
        self.assertEqual(packets[1].sequence_number, 2)
        self.assertEqual(packets[2].packet_hex, "%1604936D94000008175D")
        self.assertEqual(packets[2].sequence_number, 3)

    def test_create_raw_archive_batch_mismatch_count(self):
        invalid_payload = self.sample_payload.copy()
        invalid_payload['packet_count'] = 5  # Payload only has 3 packets
        response = self.client.post(self.url, invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(RawArchiveBatch.objects.count(), 0)
        self.assertEqual(RawPacketDetail.objects.count(), 0)
        self.assertIn('packet_count', response.data)
