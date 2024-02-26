from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import *

class ClassroomForm(ModelForm):
    class Meta:
        model = Classroom
        fields = ["name", "subject", "description", "participants"]

class SubjectForm(ModelForm):
    class Meta:
        model = Subject
        fields = "__all__"
        
class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ["body"]
        
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]