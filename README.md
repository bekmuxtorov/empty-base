# Device Monitoring System (Django Backend)

Ushbu loyiha qurilmalarni monitoring qilish (pressure, temperature, volume, battery va h.k.) va ularning ma'lumotlarini API orqali qabul qilish uchun mo'ljallangan.

## 🚀 O'rnatish va Ishga tushirish

### 1. Muhitni tayyorlash
Virtual muhitni (venv) yaratish va faollashtirish (agar yaratilmagan bo'lsa):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 2. Kutubxonalarni o'rnatish
```bash
pip install -r requirements.txt
```

### 3. Ma'lumotlar bazasini sozlash
Migratsiyalarni amalga oshirish:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Admin foydalanuvchisini yaratish
Admin panelga kirish uchun login va parol yarating:
```bash
python manage.py createsuperuser
```

### 5. Serverni ishga tushirish
```bash
python manage.py runserver
```

---

## 🛠 Ishlatish bo'yicha qo'llanma

### Admin Panel
Professional layout bilan boyitilgan admin panelga quyidagi manzil orqali kiring:
👉 **URL**: `http://127.0.0.1:8000/admin/`

Bu yerda siz qurilmalarni qo'shishingiz, tahrirlashingiz yoki filtrlash orqali kerakli ma'lumotlarni topishingiz mumkin.

### CRUD API
Barcha qurilma ma'lumotlari bilan ishlash uchun REST API tayyor:
👉 **URL**: `http://127.0.0.1:8000/api/records/`

*   `GET /api/records/` - Barcha yozuvlarni ko'rish.
*   `POST /api/records/` - Yangi ma'lumot qo'shish.
*   `GET /api/records/{id}/` - Bitta yozuvni ko'rish.
*   `PUT/PATCH /api/records/{id}/` - Mavjud yozuvni yangilash.
*   `DELETE /api/records/{id}/` - Yozuvni o'chirish.

---

## 🧪 Testlash

### Avtomatlashtirilgan testlar:
Django'ning ichki test tizimini ishga tushiring:
```bash
python manage.py test base
```

### API Test scripti:
Tayyorlangan Python scriptini ishlatib ko'ring (server yoniq bo'lishi kerak):
```bash
python api_test.py
```

---

## 📁 Loyiha tuzilishi
- `base/` - Asosiy mantiq, model va API joylashgan.
- `core/` - Loyihaning umumiy sozlamalari (`settings.py`, `urls.py`).
- `staticfiles/` - To'plangan statik fayllar.
- `api_test.py` - API test qilish uchun namuna script.
