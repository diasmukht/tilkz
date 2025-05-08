from django.contrib import admin
from .models import Course, Lesson, Question, Answer, PassedLesson

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'language', 'status')


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    ordering = ('course', 'order')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'lesson')


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct')


@admin.register(PassedLesson)
class PassedLessonAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'passed')
