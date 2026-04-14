from django.urls import path
from .views import health_check, ExcelImporter, DashboardStatsAPI, ClearDatabase, QuestionsAPI, QuestionDistributionAPI

urlpatterns = [
    path("health/", health_check, name="health"),

    # Core features
    path("upload/", ExcelImporter.as_view(), name="upload"),
    path("dashboard/", DashboardStatsAPI.as_view(), name="dashboard"),
    path("clear/", ClearDatabase.as_view(), name="clear_db"),

    # Extra system features (recommended)
    path("questions/", QuestionsAPI.as_view(), name="questions"),
    path("questions/<int:question_id>/distribution/", QuestionDistributionAPI.as_view(), name="question_distribution"),
]