import pandas as pd
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Participant, Question, SurveyResponse


@api_view(["GET"])
def health_check(request):
    return Response({"status": "ok", "message": "Survey Analytics API running"})


class ExcelImporter(APIView):
    
    def post(self, request):
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "No file provided. Use form-data key 'file'."}, status=400)

        if not file.name.lower().endswith(".xlsx"):
            return Response({"error": "Only .xlsx files are supported."}, status=400)

        try:
            df = pd.read_excel(file, engine="openpyxl", header=1).fillna("No Response")

            # MVP behavior
            SurveyResponse.objects.all().delete()
            Question.objects.all().delete()
            Participant.objects.all().delete()

            # Create participants
            participants = [Participant(identifier=f"Resp_{i+1}") for i in range(len(df))]
            Participant.objects.bulk_create(participants)
            all_p = list(Participant.objects.all().order_by("id"))

            responses_to_create = []

            for col in df.columns:
                col_str = str(col)
                col_lower = col_str.lower()

                # Basic categorization rules
                if any(w in col_lower for w in ["age", "gender", "sub city", "education", "employment"]):
                    cat = "Demographics"
                elif any(w in col_lower for w in ["learn", "telegram", "heard", "awareness"]):
                    cat = "Awareness"
                elif any(w in col_lower for w in ["topics", "skills", "training"]):
                    cat = "Training"
                elif "barrier" in col_lower:
                    cat = "Barriers"
                else:
                    cat = "General"

                q_obj = Question.objects.create(text=col_str, category=cat)

                # Create responses
                col_vals = df[col].values
                for i, val in enumerate(col_vals):
                    responses_to_create.append(
                        SurveyResponse(
                            participant=all_p[i],
                            question=q_obj,
                            answer_text=str(val),
                        )
                    )

            SurveyResponse.objects.bulk_create(responses_to_create, batch_size=1000)

            return Response({
                "status": "success",
                "rows_imported": len(df),
                "columns_imported": len(df.columns),
                "questions_created": Question.objects.count(),
                "responses_created": SurveyResponse.objects.count(),
            })

        except Exception as e:
            return Response({"error": str(e)}, status=500)


class DashboardStatsAPI(APIView):
    def get(self, request):
        def format_res(queryset):
            return [{"label": x["answer_text"], "total": x["total"]} for x in queryset]

        data = {
            "meta": {
                "participants": Participant.objects.count(),
                "questions": Question.objects.count(),
                "responses": SurveyResponse.objects.count(),
            },
            "demographics": {
                "age": format_res(
                    SurveyResponse.objects.filter(question__text__icontains="age")
                    .values("answer_text").annotate(total=Count("id"))
                    .order_by("-total")
                ),
                "gender": format_res(
                    SurveyResponse.objects.filter(question__text__icontains="gender")
                    .values("answer_text").annotate(total=Count("id"))
                    .order_by("-total")
                ),
                "location": format_res(
                    SurveyResponse.objects.filter(question__text__icontains="sub city")
                    .values("answer_text").annotate(total=Count("id"))
                    .order_by("-total")
                ),
                "employment": format_res(
                    SurveyResponse.objects.filter(question__text__icontains="employment")
                    .values("answer_text").annotate(total=Count("id"))
                    .order_by("-total")
                ),
            },
            "awareness": format_res(
                SurveyResponse.objects.filter(question__category="Awareness")
                .values("answer_text").annotate(total=Count("id"))
                .order_by("-total")[:5]
            ),
            "training": format_res(
                SurveyResponse.objects.filter(question__category="Training")
                .values("answer_text").annotate(total=Count("id"))
                .order_by("-total")[:5]
            ),
            "barriers": format_res(
                SurveyResponse.objects.filter(question__category="Barriers")
                .values("answer_text").annotate(total=Count("id"))
                .order_by("-total")[:5]
            ),
        }
        return Response(data)


class ClearDatabase(APIView):
    def post(self, request):
        SurveyResponse.objects.all().delete()
        Question.objects.all().delete()
        Participant.objects.all().delete()
        return Response({"status": "Database cleared successfully"})


class QuestionsAPI(APIView):
    def get(self, request):
        qs = Question.objects.all().order_by("category", "id").values("id", "text", "category")
        return Response(list(qs))


class QuestionDistributionAPI(APIView):
   
    def get(self, request, question_id: int):
        if not Question.objects.filter(id=question_id).exists():
            return Response({"error": "Question not found"}, status=404)

        counts = (
            SurveyResponse.objects.filter(question_id=question_id)
            .values("answer_text")
            .annotate(total=Count("id"))
            .order_by("-total")
        )

        labels = [x["answer_text"] for x in counts]
        values = [x["total"] for x in counts]

        q = Question.objects.get(id=question_id)
        return Response({
            "question_id": q.id,
            "question_text": q.text,
            "category": q.category,
            "labels": labels,
            "values": values,
        })