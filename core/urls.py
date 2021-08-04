from django.urls import path
from .views import (
HomeView,
ExamView,
CourseView,
CourseCreateView,
course_single,
CourseAssignmentListView,
AssignmentCreateView,
AssignmentView,
AssignmentDeleteView,
ExamCreateView,
ExamListView,
AssignmentSubmissionView,
AssignmentSubmissionUpdateView,
AssignmentDetailView,
ExamDeleteView,
ExamSubmissionView,
ExamSubmissionListView,
AssignmentSubmissionListView,
AssignmentSubmissionDelete,
ExamSubmissionDelete

)
from django.conf import settings
from django.conf.urls.static import static

app_name = "core"

urlpatterns = [
                  path('', HomeView.as_view(), name='home'),
                  # Exams URLs
                  path('exam/', ExamView.as_view(), name='exam'),
                  path('exam-create/', ExamCreateView.as_view(), name='exam-create'),
                  path('exam-list/', ExamListView.as_view(), name='exam-list'),
                  path('<pk>/delete/', ExamDeleteView.as_view(), name='delete-exam'),
                  path('exam-submission/', ExamSubmissionView.as_view(), name='exam-submission'),
                  path('exam-submission-list/', ExamSubmissionListView.as_view(), name='exam-submission-list'),
                  path('<pk>/delete/', ExamSubmissionDelete.as_view(), name='exam-submission-delete'),

                  # Course URLs
                  path('course/', CourseView.as_view(), name='course'),
                  path('course-create/', CourseCreateView.as_view(), name='course-create'),
                  path('<str:course_code>/course-view/', course_single, name='course-view'),
                  path('course_<int:id>/assignment-view/', CourseAssignmentListView, name='assignment-view'),

                  # Assignment URLs
                  path('assignment-create/', AssignmentCreateView.as_view(), name='assignment-create'),
                  path('assignments/', AssignmentView.as_view(), name='assignment-list'),
                  path('assignment/<int:pk>/', AssignmentDetailView.as_view(), name='assignment-detail'),
                  path('<pk>/delete/', AssignmentDeleteView.as_view(), name='delete-assignment'),
                  path('assignment-submission/', AssignmentSubmissionView.as_view(), name='assignment-submission'),
                  path('assignment-submission-list/', AssignmentSubmissionListView.as_view(), 
                        name='assignment-submission-list'),
                  path('assignment-submission/<int:pk>/mark', AssignmentSubmissionUpdateView.as_view(), name='assignment-submission-update'),
                  path('<pk>/delete/', AssignmentSubmissionDelete.as_view(), name='assignment-submission-delete'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
