from django.db import models

# Create your models here.
class Chapters(models.Model):
    number=models.IntegerField()
    title=models.CharField(max_length=50)
    description=models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Topics(models.Model):
    chapter=models.ForeignKey(
        Chapters,
        on_delete=models.CASCADE,
        related_name="topics"
    )
    title=models.CharField(max_length=100)
    category=models.CharField(max_length=50,default="General")
    content=models.TextField()
    example_code=models.TextField(blank=True)
    order=models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Interview(models.Model):
    chapter=models.ForeignKey(
        Chapters,
        on_delete=models.CASCADE,
        related_name="interview"
    )
    title=models.CharField(max_length=100)

    def __str__(self):
        return self.title

class CodingQuestion(models.Model):
    chapter = models.ForeignKey(
        Chapters,
        on_delete=models.CASCADE,
        related_name="coding_questions"
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    starter_code = models.TextField(blank=True)
    expected_output = models.TextField(blank=True)

    def __str__(self):
        return self.title