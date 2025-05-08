from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Course(models.Model):
    title = models.CharField(max_length=255)
    language = models.CharField(max_length=50, default="Орыс тілі")
    status = models.CharField(max_length=50, choices=[
        ('free', 'Тегін'),
        ('advanced', 'Тек advanced үшін')
    ])
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    video_url = models.URLField()
    order = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.course.title} — {self.title}"


class Question(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text} ({'дұрыс' if self.is_correct else 'қате'})"


class PassedLesson(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    passed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'lesson')
