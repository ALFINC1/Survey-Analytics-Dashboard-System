import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response as DRFResponse
from .models import Participant, Question, SurveyResponse
from django.db.models import Count

class ExcelImporter(APIView):
    def post(self, request):
        file = request.FILES.get('file')
        if not file: 
            return DRFResponse({"error": "No file"}, status=400)
            
        try:
            df = pd.read_excel(file, engine='openpyxl', header=1).fillna("No Response")
            
            Participant.objects.all().delete()
            Question.objects.all().delete()

            participants = [Participant(identifier=f"Resp_{i}") for i in range(len(df))]
            Participant.objects.bulk_create(participants)
            all_p = list(Participant.objects.all().order_by('id'))

            responses_to_create = []

            for col in df.columns:
                col_str = str(col)
                col_lower = col_str.lower()
                
                if any(w in col_lower for w in ['age', 'gender', 'sub city', 'education', 'employment']):
                    cat = "Demographics"
                elif any(w in col_lower for w in ['learn', 'telegram', 'heard', 'awareness']):
                    cat = "Awareness"
                elif any(w in col_lower for w in ['topics', 'skills', 'training']):
                    cat = "Training"
                elif "barrier" in col_lower:
                    cat = "Barriers"
                else: 
                    cat = "General"

                q_obj = Question.objects.create(text=col_str, category=cat)

                col_vals = df[col].values
                for i, val in enumerate(col_vals):
                    responses_to_create.append(
                        SurveyResponse(
                            participant=all_p[i],
                            question=q_obj,
                            answer_text=str(val)
                        )
                    )

            SurveyResponse.objects.bulk_create(responses_to_create, batch_size=1000)

            return DRFResponse({"status": "Success"}, status=200)

        except Exception as e:
            return DRFResponse({"error": str(e)}, status=500)

class DashboardStatsAPI(APIView):
    def get(self, request):
        def format_res(queryset):
            return [{"label": x['answer_text'], "total": x['total']} for x in queryset]

        data = {
            "demographics": {
                "age": format_res(SurveyResponse.objects.filter(question__text__icontains="age").values('answer_text').annotate(total=Count('id'))),
                "gender": format_res(SurveyResponse.objects.filter(question__text__icontains="gender").values('answer_text').annotate(total=Count('id'))),
                "location": format_res(SurveyResponse.objects.filter(question__text__icontains="sub city").values('answer_text').annotate(total=Count('id'))),
                "employment": format_res(SurveyResponse.objects.filter(question__text__icontains="employment").values('answer_text').annotate(total=Count('id'))),
            },
            "awareness": format_res(SurveyResponse.objects.filter(question__category="Awareness").values('answer_text').annotate(total=Count('id')).order_by('-total')[:5]),
            "training": format_res(SurveyResponse.objects.filter(question__category="Training").values('answer_text').annotate(total=Count('id')).order_by('-total')[:5]),
            "barriers": format_res(SurveyResponse.objects.filter(question__category="Barriers").values('answer_text').annotate(total=Count('id')).order_by('-total')[:5]),
        }
        return DRFResponse(data) 

class ClearDatabase(APIView):
    def post(self, request):
        Participant.objects.all().delete()
        Question.objects.all().delete()
        return DRFResponse({"status": "Database cleared successfully"})