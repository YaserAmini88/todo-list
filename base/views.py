from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView

from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Task

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True # if user is authenticated, this page cannot be seen.

    def get_success_url(self):        # When user logged in, redirect to tasks page
        return reverse_lazy('tasks')


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm     # A form to creat users
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):   # form functionality
        user = form.save()
        if user is not None:       #after creation of user login and redirect it.
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):  #if user is logged in, it cannot see login and register page and will be redirected to tasks page.
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)



class TaskList(LoginRequiredMixin, ListView):     # By default django looks for task(model name)_list.html template
    model = Task                                  # LoginRequiredMixin - Restriction if user is not logged in. if someone wants to see detail view of an object
                                                  # but is not logged in, redirect to login page which is set in settings.py
    context_object_name = 'tasks'                 # overriding default name for queryset - default name is object_list

    def get_context_data(self, **kwargs):         # Each user can only see their tasks
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()  # count is a variable in task_list.html
        #Search functionality
        search_input = self.request.GET.get('search-area') or '' # search-area is defined in html form
        if search_input:
            #context['tasks'] = context['tasks'].filter(title__icontains=search_input)
            context['tasks'] = context['tasks'].filter(title__startswith=search_input)

        context['search_input'] = search_input
        return context

class TaskDetail(LoginRequiredMixin, DetailView): # By default looks for task(model name)_detail.html template -
                                                  # LoginRequiredMixin : if someone wants to see detail view of an object
                                                  # but is not logged in, redirect to login page which is set in settings.py
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'

class TaskCreate(LoginRequiredMixin, CreateView): #Create an object in db - By default it looks for task(model_name)_form.html template.
    model = Task
    #form_class = TaskForm       => Create our own model form
    fields = ['user', 'title','description', 'complete']   # Remove user field - Because of def form_valid
    success_url = reverse_lazy('tasks') #If everything goes ok redirect to tasks, which is defined in "name" filed in urls file.

    # Each user can only add tasks for itself not others - User field in add task must be equal to logged in user
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

    # When adding an item, put the user equal to logged in user.
    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user.pk
        return initial

class TaskUpdate(LoginRequiredMixin, UpdateView):  # Modify the data in db - By default it looks for task(model_name)_form.html template.
    model = Task
    fields = ['title','description', 'complete']
    success_url = reverse_lazy('tasks')

class TaskDelete(LoginRequiredMixin, DeleteView):  #By default it looks for task(model_name)_confirm_delete.htmlss
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')


