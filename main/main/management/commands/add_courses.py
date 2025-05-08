from django.core.management.base import BaseCommand
from main.models import Course, Lesson, Question, Answer
import random
import string

class Command(BaseCommand):
    help = 'Автоматты түрде 6 курс пен сабақтарды базаға қосады'

    def handle(self, *args, **kwargs):
        topics = [
            "Жалпы шолу",
            "Окончания и род",
            "Падеж",
            "Предлог",
            "Приставка",
            "Глагол"
        ]

        for i, title in enumerate(topics, 1):
            slug = ''.join(random.choices(string.ascii_lowercase, k=8))
            course = Course.objects.create(
                title=title,
                language="Орыс тілі",
                status="advanced",
                slug=slug
            )
            lesson_count = random.randint(4, 8)
            for j in range(1, lesson_count + 1):
                lesson = Lesson.objects.create(
                    course=course,
                    title=f"{title} – Сабақ {j}",
                    video_url=f"https://example.com/{i}-{j}",
                    order=j
                )
                for q in range(1, 6):
                    question = Question.objects.create(
                        lesson=lesson,
                        text=f"{title} Сабақ {j} – Сұрақ {q}?"
                    )
                    for a in range(3):
                        Answer.objects.create(
                            question=question,
                            text=f"Нұсқа {a+1}",
                            is_correct=(a == 0)
                        )

        self.stdout.write(self.style.SUCCESS('✅ Курстар, сабақтар, тесттер сәтті қосылды!'))
