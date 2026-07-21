# Device Monitoring API Qo'llanmasi

Ushbu loyiha uchun REST API `http://127.0.0.1:8000/api/records/` manzili orqali ishlaydi. Quyida CRUD amallarining batafsil tavsifi keltirilgan.

## 1. Barcha yozuvlarni olish (List)
Barcha saqlangan qurilma ma'lumotlarini ro'yxat ko'rinishida olish.

*   **URL**: `/api/records/`
*   **Method**: `GET`
*   **Response**: `200 OK`
```json
[
  {
    "id": 1,
    "device_id": "DEV-01",
    "status": "online",
    "timestamp": "2024-03-28T21:00:00Z",
    ...
  }
]
```

## 2. Yangi yozuv qo'shish (Create)
Qurilmadan serverga yangi ma'lumot yuborish.

*   **URL**: `/api/records/`
*   **Method**: `POST`

### Standart holat (online):
*   **Request Body**:
```json
{
  "device_id": "DEV-001",
  "meter_id": "MTR-123",
  "phone": "+998901234567",
  "pressure": 1.5,
  "temperature": 25.4,
  "volume": 120.5,
  "signal": 95,
  "battery": 88.0,
  "status": "online",
  "timestamp": "2024-03-28T21:05:00Z"
}
```
*   **Response**: `201 Created`

### Schotchik javob bermagan holat (no response):
*   **Request Body**:
```json
{
  "device_id": "DEV-002",
  "meter_id": "MTR-5555",
  "phone": "+998901644101",
  "archive_type": "daily",
  "raw_hex": "",
  "status": "meter_no_response",
  "message": "Schotchik javob bermadi"
}
```
*   **Response**: `201 Created`

## 3. Bitta yozuvni ko'rish (Detail)
ID orqali aniq bir yozuv ma'lumotini olish.

*   **URL**: `/api/records/{id}/`
*   **Method**: `GET`
*   **Response**: `200 OK`

## 4. Yozuvni yangilash (Update)
Mavjud yozuvni to'liq yoki qisman o'zgartirish.

*   **URL**: `/api/records/{id}/`
*   **Method**: `PUT` (To'liq) yoki `PATCH` (Qisman)
*   **Request Body (PATCH)**:
```json
{
  "status": "offline",
  "battery": 15.0
}
```
*   **Response**: `200 OK`

## 5. Yozuvni o'chirish (Delete)
Ma'lumotlar bazasidan yozuvni olib tashlash.

*   **URL**: `/api/records/{id}/`
*   **Method**: `DELETE`
*   **Response**: `204 No Content`

---

## 📝 Maydonlar tavsifi (Field Descriptions)

| Maydon | Turi | Tavsif |
| :--- | :--- | :--- |
| `device_id` | String | Qurilmaning noyob identifikatori (Majburiy) |
| `meter_id` | String | Hisoblagich ID raqami (Ixtiyoriy) |
| `phone` | String | Aloqa uchun telefon raqami |
| `pressure` | Float | Bosim ko'rsatkichi (Standart: 0) |
| `temperature`| Float | Harorat ko'rsatkichi (Standart: 0) |
| `volume` | Float | Hajm ko'rsatkichi (Standart: 0) |
| `signal` | Integer | Signal kuchi (%) |
| `battery` | Float | Batareya quvvati (%) |
| `status` | String | Qurilma holati (masalan, `online`, `offline`, `meter_no_response`) |
| `archive_type` | String | So'ralgan arxiv turi (masalan, `daily`, `hourly`) |
| `raw_hex` | String | Qurilmadan olingan xom hex ma'lumoti |
| `message` | String | Xatolik yoki holat haqidagi batafsil xabar (masalan, `Schotchik javob bermadi`) |
| `timestamp` | DateTime| Qurilmada qayd etilgan vaqt (ISO format, offline/no-response holatlarida ixtiyoriy) |
| `created_at` | DateTime| Serverga kelib tushgan vaqt (Avtomatik) |

---

# BK Gaz Hisoblagichi API Qo'llanmasi

Ushbu qismda BK gaz hisoblagichidan keladigan ma'lumotlarni saqlash va o'qish uchun yaratilgan API endpoints tavsifi keltirilgan.

## 1. Ma'lumotlarni qabul qilish (Ingest API)

Gaz hisoblagichi o'z arxividagi barcha (yoki qisman) ma'lumotlarni bitta JSON qilib yuboradi. Server bu barcha ma'lumotlarni tartiblab alohida arxiv jadvallarga yozib chiqadi.

*   **URL**: `/bkgaz/ingest/`
*   **Method**: `POST`
*   **Request Body**:
```json
{
  "meta": {
    "device_address": "1",
    "port": "COM1"
  },
  "current": {
    "timestamp": "2026-05-24T10:28:00",
    "work_volume": 2165372.0,
    "pressure": 1.0335
  },
  "hourly": {
    "records": [
      {
        "timestamp": "2026-05-13T22:00:00",
        "pressure": 1.033500,
        "acc_work_vol": 2165250.0
      }
    ]
  }
}
```
*   **Response**: `201 Created`

## 2. Arxiv va holatlarni o'qish (Read APIs)

Ma'lumotlar turiga qarab alohida REST API manzillari mavjud. Bu manzillarda `GET` so'rovlari orqali ro'yxatni (List) yoki ma'lum bir ID'dagi yozuvni (Detail) o'qib olish mumkin.

**Barcha arxiv turlari uchun manzillar:**
1. **Joriy holat**: `/bkgaz/current/`
2. **Soatlik arxiv**: `/bkgaz/hourly/`
3. **Kunlik arxiv**: `/bkgaz/daily/`
4. **Oylik arxiv**: `/bkgaz/monthly/`
5. **Favqulodda xolatlar**: `/bkgaz/emergency/`
6. **O'zgaruvchilar**: `/bkgaz/variable/`

**Namuna (Joriy holatlarni ro'yxatini olish):**
*   **URL**: `/bkgaz/current/`
*   **Method**: `GET`
*   **Response**: `200 OK`
```json
[
  {
    "id": 1,
    "device_address": "1",
    "timestamp": "2026-05-24T10:28:00Z",
    "work_volume": 2165372.0,
    "pressure": 1.0335,
    "temperature": 18.75,
    "emergency_active": false,
    "emergency_codes": []
  }
]
```

> **Eslatma**: Dastlab o'qish API'lari faqat o'qish uchun mo'ljallangan edi, lekin hozir ularning barchasi `ModelViewSet` ga o'zgartirildi. Ya'ni siz `/bkgaz/current/`, `/bkgaz/hourly/` kabi manzillarga to'g'ridan-to'g'ri `POST`, `PUT`, `PATCH`, `DELETE` so'rovlarini yuborib, alohida jadvallarga bitta-bitta obyekt qo'shishingiz, tahrirlashingiz yoki o'chirishingiz ham mumkin.

---

# Xom Hex Paketlarini Ingest Qilish API

Ushbu bo'limda qurilmadan keladigan xom hex paketlarini to'plam (batch) ko'rinishida yuborish va bazada normalized holda saqlash uchun API tavsifi berilgan.

## 1. Paket to'plamini yuborish (Ingest)

*   **URL**: `/api/raw-packets/`
*   **Method**: `POST`
*   **Headers**: `Content-Type: application/json`
*   **Request Body**:
```json
{
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
```

*   **Muvaffaqiyatli Javob (201 Created)**:
```json
{
  "id": 1,
  "device_id": "DEV-002",
  "meter_id": "MTR-5555",
  "archive_type": "monthly",
  "start_address": "6086",
  "end_address": "6279",
  "packet_count": 3,
  "packets": [
    {
      "id": 1,
      "sequence_number": 1,
      "packet_hex": "%1600000816000000002D",
      "created_at": "2026-07-21T09:39:24.123456Z"
    },
    {
      "id": 2,
      "sequence_number": 2,
      "packet_hex": "%16000000000495F02957",
      "created_at": "2026-07-21T09:39:24.125678Z"
    },
    {
      "id": 3,
      "sequence_number": 3,
      "packet_hex": "%1604936D94000008175D",
      "created_at": "2026-07-21T09:39:24.127890Z"
    }
  ],
  "created_at": "2026-07-21T09:39:24.121234Z"
}
```

*   **Xatolik Javobi (400 Bad Request)** (agar `raw_packets` ro'yxati uzunligi `packet_count` ga mos kelmasa):
```json
{
  "packet_count": [
    "Paketlar soni (3) packet_count (5) ga mos kelmaydi."
  ]
}
```

## 2. Saqlangan paket to'plamlarini o'qish (Read)

*   **URL**: `/api/raw-packets/`
*   **Method**: `GET`
*   **Response**: `200 OK`

*   **Bitta to'plam tafsilotlarini ko'rish**:
    *   **URL**: `/api/raw-packets/{id}/`
    *   **Method**: `GET`
    *   **Response**: `200 OK`

