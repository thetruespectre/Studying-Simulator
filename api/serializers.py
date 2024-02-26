from rest_framework.serializers import ModelSerializer
from base.models import *

class ClassroomSerialzer(ModelSerializer):
    class Meta:
        model = Classroom
        fields = "__all__"
        
class UserSerialzer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"