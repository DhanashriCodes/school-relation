
from django.urls import path
from . import views

urlpatterns = [
    path('std/',views.handleStudent),
    path('teacher/',views.handleTeacher),
    path('teacher/<int:id>/classroom/', views.handleTeacherClassRoom2),
    path('classroom/',views.handleClassroom)
]