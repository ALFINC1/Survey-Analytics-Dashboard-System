from django.urls import path
from .views import ExcelImporter, DashboardStatsAPI, ClearDatabase

urlpatterns = [
    path('import/', ExcelImporter.as_view(), name='import'),
    path('stats/', DashboardStatsAPI.as_view(), name='stats'),
    path('clear/', ClearDatabase.as_view(), name='clear'),
]