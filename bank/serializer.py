from rest_framework import serializers
from .models import Users,Requests


#---------------User---------------

class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model = Users
        fields = ['email','password','username','password2','status','name','cell_no','role','aadhar_id','PAN_no']
        extra_kwargs = {
                    'password': {'write_only':True},
        }
    def save(self):
        register = Users(
                    email=self.validated_data['email'],
                    username=self.validated_data['username'],
                    name = self.validated_data['name'],
                    cell_no = self.validated_data['cell_no'],
                    role = self.validated_data['role'],
                    aadhar_id = self.validated_data['aadhar_id'],
                    PAN_no = self.validated_data['PAN_no']
                )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password':'Password must be match'})  
        register.set_password(password)
        register.save()
        return register


#-----------Request---------

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requests
        fields = ['agent_name','user_name','loan_amt','interest_rate','EMI','total_months','status','generated_at','updated_at']

