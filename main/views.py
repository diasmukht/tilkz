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
