from django.db import models

class Participant(models.Model):
    identifier = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.identifier

class Question(models.Model):
    text = models.TextField()
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.text

class SurveyResponse(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField()

    def __str__(self):
        return f"{self.participant.identifier} - {self.question.text[:20]}"