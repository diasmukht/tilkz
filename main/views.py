from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Lesson, Question, Answer, PassedLesson
from django.contrib.auth.decorators import login_required
from django.db.models import Count

@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'main/course_list.html', {'courses': courses})


@login_required
def lesson_detail(request, course_slug, lesson_order):
    course = get_object_or_404(Course, slug=course_slug)
    
    if course.status == 'advanced' and request.user.profile.status != 'advanced':
        return render(request, 'main/access_denied.html')

    lesson = get_object_or_404(Lesson, course=course, order=lesson_order)

    # Алдыңғы сабақ өтілген бе?
    if lesson.order > 1:
        prev_lesson = Lesson.objects.get(course=course, order=lesson.order - 1)
        passed = PassedLesson.objects.filter(user=request.user, lesson=prev_lesson, passed=True).exists()
        if not passed:
            return render(request, 'main/locked_lesson.html', {'lesson': prev_lesson})

    questions = Question.objects.filter(lesson=lesson).prefetch_related('answer_set')

    if request.method == 'POST':
        score = 0
        total = questions.count()
        for question in questions:
            selected_id = request.POST.get(f"question_{question.id}")
            if selected_id:
                answer = Answer.objects.get(id=selected_id)
                if answer.is_correct:
                    score += 1
        passed = score >= int(0.8 * total)

        PassedLesson.objects.update_or_create(
            user=request.user,
            lesson=lesson,
            defaults={'passed': passed}
        )
        return render(request, 'main/test_result.html', {
            'lesson': lesson,
            'score': score,
            'total': total,
            'passed': passed
        })

    return render(request, 'main/lesson_detail.html', {
        'course': course,
        'lesson': lesson,
        'questions': questions
    })
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from .models import Course, Lesson, Question, Answer
import random
import string

@staff_member_required
def add_courses_view(request):
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
            for q in range(1, 5):
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

    return HttpResponse("✅ Курстар сәтті қосылды!")
