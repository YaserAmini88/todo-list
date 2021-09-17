from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView, DeleteView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Task

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):        # When user logged in, redirect to tasks page
        return reverse_lazy('tasks')

class TaskList(LoginRequiredMixin, ListView):     # By default looks for task(model name)_list.html template
    model = Task                                  # LoginRequiredMixin - Restriction if user is not logged in
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):         # Each user can only see their tasks
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        return context

class TaskDetail(LoginRequiredMixin, DetailView): # By default looks for task(model name)_detail.html template -
                                                  # LoginRequiredMixin : if someone wants to see detail view of an object
                                                  # but is not logged in, redirect to login page which is set in settings.py
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title','description', 'complete']   # Remove user field - Because of def form_valid
    success_url = reverse_lazy('tasks') #If everything goes ok redirect to tasks, which is defined in "name" filed in urls file.

    # Each user can only add tasks for itself not others - User field in add task must be equal to logged in user
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):  # Modify the data
    model = Task
    fields = ['title','description', 'complete']
    success_url = reverse_lazy('tasks')

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')


