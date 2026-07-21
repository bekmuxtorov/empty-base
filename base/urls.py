from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DataRecordViewSet, BKGazDataIngestView, BKGazCurrentDataViewSet,
    BKGazHourlyArchiveViewSet, BKGazDailyArchiveViewSet, BKGazMonthlyArchiveViewSet,
    BKGazEmergencyArchiveViewSet, BKGazVariableArchiveViewSet,
    RawArchiveBatchViewSet
)

router = DefaultRouter()
router.register(r'records', DataRecordViewSet, basename='datarecord')
router.register(r'bkgaz/current', BKGazCurrentDataViewSet, basename='bkgaz-current')
router.register(r'bkgaz/hourly', BKGazHourlyArchiveViewSet, basename='bkgaz-hourly')
router.register(r'bkgaz/daily', BKGazDailyArchiveViewSet, basename='bkgaz-daily')
router.register(r'bkgaz/monthly', BKGazMonthlyArchiveViewSet, basename='bkgaz-monthly')
router.register(r'bkgaz/emergency', BKGazEmergencyArchiveViewSet, basename='bkgaz-emergency')
router.register(r'bkgaz/variable', BKGazVariableArchiveViewSet, basename='bkgaz-variable')
router.register(r'raw-packets', RawArchiveBatchViewSet, basename='raw-packets')

urlpatterns = [
    path('bkgaz/ingest/', BKGazDataIngestView.as_view(), name='bkgaz-ingest'),
    path('', include(router.urls)),
]
