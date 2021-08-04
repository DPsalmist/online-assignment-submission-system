from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, CreateView, ListView, DeleteView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from authentication.decorators import user_is_instructor, user_is_student

from .forms import CourseCreateForm, AssignmentCreateForm, ExamCreateForm, AssignmentSubmissionForm, ExamSubmissionForm
from .models import Course, Assignment, Exam, ExamSubmission, AssignmentSubmission


# Home View
class HomeView(ListView):
    paginate_by = 6
    template_name = 'home.html'
    model = Course
    context_object_name = 'course'

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['assignment_notification'] = Assignment.objects.filter(status='Incomplete').count()
        return context


''' ALL COURSES VIEW '''

# COURSE CREATE VIEW
class CourseCreateView(CreateView):
    template_name = 'core/instructor/course_create.html'
    form_class = CourseCreateForm
    extra_context = {
        'title': 'New Course'
    }
    success_url = reverse_lazy('core:course')

    @method_decorator(login_required(login_url=reverse_lazy('authentication:login')))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('authentication:login')
        if self.request.user.is_authenticated and self.request.user.role != 'instructor':
            return reverse_lazy('authentication:login')
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CourseCreateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

# COURSE LIST VIEW
class CourseView(ListView):
    model = Course
    template_name = 'core/instructor/courses.html'
    context_object_name = 'course'

    @method_decorator(login_required(login_url=reverse_lazy('authentication:login')))
    # @method_decorator(user_is_instructor, user_is_student)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.all().order_by('id')  # filter(user_id=self.request.user.id).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super(CourseView, self).get_context_data(**kwargs)
        context['assignment_notification'] = Assignment.objects.filter(status='Incomplete').count()
        return context

# SINGLE COURSE VIEW
def course_single(request, course_code):
    course = get_object_or_404(Course, course_code=course_code)
    current_course_code = course.course_code   
    this_assignment = Assignment.objects.filter(assignment_course__course_code=current_course_code)
    assignment_notification = Assignment.objects.filter(status='Incomplete').count()
    context = {
        'assignment_notification': assignment_notification,
        'course': course,
        'this_assignment': this_assignment,
    }
    return render(request, "core/instructor/view_course.html", context)


''' ALL ASSIGNMENT VIEWS '''

# ASSIGNMENT CREATE VIEW
class AssignmentCreateView(CreateView):
    template_name = 'core/instructor/assignment_create.html'
    form_class = AssignmentCreateForm
    extra_context = {
        'title': 'New Course'
    }
    success_url = reverse_lazy('core:assignment-list')

    @method_decorator(login_required(login_url=reverse_lazy('authentication:login')))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('authentication:login')
        if self.request.user.is_authenticated and self.request.user.role != 'instructor':
            return reverse_lazy('authentication:login')
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AssignmentCreateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


# ASSIGNMENT LIST VIEW
class AssignmentView(ListView):
    model = Assignment
    template_name = 'core/instructor/assignments.html'
    context_object_name = 'assignment'

    @method_decorator(login_required(login_url=reverse_lazy('authentication:login')))
    # @method_decorator(user_is_student, user_is_instructor)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.all()  # filter(user_id=self.request.user.id).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super(AssignmentView, self).get_context_data(**kwargs)
        context['assignment_notification'] = Assignment.objects.filter(status='Incomplete').count()
        return context

# ASSIGNMENT UPDATE VIEW
class AssignmentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = AssignmentSubmission
    fields = ['user','title','assignment_course', 'content', 'marks',
                'status', 'duration']
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    #test function to make only an authorised user update an assignment
    def test_func(self):
        assignment = self.get_object()
        if self.request.user == assignment.assignment_course.user:
            return True
        return False


# COURSE ASSIGNMENT VIEW
class CourseAssignmentListView(ListView):
    model =  Assignment
    template_name = 'core/assignment_detail.html' 
    context_object_name = 'course_assignment'
    ordering = ['-created_at'] 
    paginate_by = 3

    def get_queryset(self):
        return self.model.objects.all().order_by('id')

# ASSIGNMENT DETAIL VIEW
class AssignmentDetailView(DetailView):
    model = Assignment

    def get_context_data(self, **kwargs):
        context = super(AssignmentDetailView, self).get_context_data(**kwargs)
        context['assignment_notification'] = Assignment.objects.filter(status='Incomplete').count()
        return context

# ASSIGNMENT DELETE VIEW
class AssignmentDeleteView(DeleteView):
    model = Assignment
    success_url = reverse_lazy('core:assignment-list')


# ASSIGNMENT SUBMISSION VIEW
class AssignmentSubmissionView(CreateView):
    template_name = 'core/instructor/assignment_submission.html'
    form_class = AssignmentSubmissionForm
    extra_context = {
        'title': 'New Assignment'
    }
    success_url = reverse_lazy('core:home')

    @method_decorator(login_required(login_url=reverse_lazy('authentication:login')))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('authentication:login')
        if self.request.user.is_authenticated and self.request.user.role != 'student':
            return reverse_lazy('authentication:login')
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AssignmentSubmissionView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

# Assignment SUBMISSON LIST VIEW
class AssignmentSubmissionListView(ListView):
    model = AssignmentSubmission
    template_name = 'core/instructor/assignment_submission_list.html'
    context_object_name = 'assignment_submission'

        # To get the current user
    def get_object(self):
        current_user = self.request.user
        print ('Here it is:', 'assignment_submission', current_user )
        return current_user

    @method_decorator(login_required(login_url=reverse_lazy('authentication:login')))
    # @method_decorator(user_is_instructor, user_is_student)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.all().order_by('-id')  # filter(user_id=self.request.user.id).order_by('-id')

# ASSIGNMENT SUBMISSION UPDATE VIEW
class AssignmentSubmissionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = AssignmentSubmission
    fields = ['user', 'assignment_course_code','assignment_course', 'content', 'file']
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    #test function to make only an authorised user update an assignment
    def test_func(self):
        assignment = self.get_object()
        if self.request.user == assignment.assignment_course.user:
            return True
        return False

# ASSIGNMENT SUBMISSION DELETE VIEW
class AssignmentSubmissionDelete(DeleteView):
    model = AssignmentSubmission
    success_url = reverse_lazy('core:assignment-submission-list')


''' ALL EXAM VIEWS '''

# EXAM VIEW
class ExamView(TemplateView):
    template_name = 'core/exams.html'

# EXAM CREATE VIEW
class ExamCreateView(CreateView):
    template_name = 'core/instructor/exam_create.html'
    form_class = ExamCreateForm
    extra_context = {
        'title': 'New Exam'
    }
    success_url = reverse_lazy('core:exam-list')

    @method_decorator(login_required(login_url=reverse_lazy('authentication:login')))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('authentication:login')
        if self.request.user.is_authenticated and self.request.user.role != 'instructor':
            return reverse_lazy('authentication:login')
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ExamCreateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

# EXAM LIST VIEW
class ExamListView(ListView):
    model = Exam
    template_name = 'core/instructor/exam_list.html'
    context_object_name = 'exam'

    @method_decorator(login_required(login_url=reverse_lazy('authentication:login')))
    # @method_decorator(user_is_instructor)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.all().order_by('-id')  # filter(user_id=self.request.user.id).order_by('-id')

# EXAM DELETE VIEW
class ExamDeleteView(DeleteView):
    model = Exam
    success_url = reverse_lazy('core:exam-list')

# EXAM SUBMISSION VIEW
class ExamSubmissionView(CreateView):
    template_name = 'core/instructor/exam_submission.html'
    form_class = ExamSubmissionForm
    extra_context = {
        'title': 'New Exam'
    }
    success_url = reverse_lazy('core:home')

    @method_decorator(login_required(login_url=reverse_lazy('authentication:login')))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('authentication:login')
        if self.request.user.is_authenticated and self.request.user.role != 'student':
            return reverse_lazy('authentication:login')
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ExamSubmissionView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

#  EXAM SUBMISSION LIST VIEW
class ExamSubmissionListView(ListView):
    model = ExamSubmission
    template_name = 'core/instructor/exam_submission_list.html'
    context_object_name = 'exam_submission'

    @method_decorator(login_required(login_url=reverse_lazy('authentication:login')))
    # @method_decorator(user_is_instructor, user_is_student)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.all().order_by('-id')  # filter(user_id=self.request.user.id).order_by('-id')

# EXAM DELETE VIEW
class ExamSubmissionDelete(DeleteView):
    model = ExamSubmission
    success_url = reverse_lazy('core:exam-submission-list')
