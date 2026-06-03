from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import DataRecord
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
