from django.db import models
from django.contrib.auth.models import User #Default user model for handling username, password, email, ...

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) #on_delete = if user is deleted, all tasks will be deleted too.
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)    #Time that task was created - this field will be hidden

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complete']              # Order task by complete field - complete tasks go to bottom of the list.
