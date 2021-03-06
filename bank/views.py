from django.shortcuts import render
from .serializer import RequestSerializer,UserSerializer
from .models import Requests,Users

from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token


#---------User(RUD)------------------       
 
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def UsersCreate(request):
    logger = request.user
    if logger.role == 'Admin':
        if request.method == 'GET':
            users = Users.objects.all()
            serializer = UserSerializer(users,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
    else:
        return Response({'response':"You don't have permission."})

@api_view(['GET','PUT','DELETE'])
@permission_classes((IsAuthenticated,))
def UsersView(request,pk):
    try:
        users=Users.objects.get(pk=pk)
    except Users.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    logger = request.user
    if logger.role == 'Admin':
        if request.method == 'GET':
            serializer = UserSerializer(users)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = UserSerializer(users,data=request.data)
            data={}
            if serializer.is_valid():
                serializer.save()
                data['success'] = 'Updated Successfully'
                return Response(data=data)
            return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)

        elif request.method == 'DELETE':
            operation = users.delete()
            data = {}
            if operation:
                data['success'] = 'Deleted Done'
            else:
                data['failure'] = 'Failed'
            return Response(data=data)
    else:
        return Response({'response':"You don't have permission."})


#---------------Register(User create)---------------

@api_view(['POST'])
def Registration(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        data={}
        if serializer.is_valid():
            register = serializer.save()
            data['response'] = 'successfully registered'
            data['email']  = register.email
            data['username'] = register.username
            data['name'] = register.name
            data['role'] = register.role
            data['aadhar id'] = register.aadhar_id
            data['PAN_no'] = register.PAN_no
            data['cell no']= register.cell_no
            data['status'] = register.status
            token = Token.objects.get(user=register).key
            data['token'] = token
        else:
            data = serializer.errors  
        return Response(data) 


#----------------Request(CRUD)------------

@api_view(['GET','POST'])
@permission_classes((IsAuthenticated,))
def RequestsCreate(request):
    logger = request.user
    if logger.role == 'Admin': 
        if request.method == 'GET':
            requests = Requests.objects.all()
            serializer = RequestSerializer(requests,many=True)
            return Response(serializer.data)
    else:
        return Response({'response':"You don't have permission."})
    
    if logger.role == 'Agent':
        if request.method == 'POST':
            requests = RequestSerializer(data = request.data)
            data={}
            if requests.is_valid():
                r=requests.save()
                data['user_name']=r.user_name.name
                data['agent_name']=r.agent_name.name
                data['loan_amt']=r.loan_amt
                data['interest_rate']=r.interest_rate
                data['EMI']=r.EMI
                data['total_months']=r.total_months
                return Response(requests.data, status=status.HTTP_201_CREATED)
            return Response(requests.errors,status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'response':"You don't have permission."})


@api_view(['GET','PUT','DELETE'])
@permission_classes((IsAuthenticated,))
def RequestsView(request,pk):
    try:
        requests=Requests.objects.get(pk=pk)
    except Requests.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    logger = request.user
    if logger == requests.user_name or logger == requests.agent_name:
        if request.method == 'GET':
            serializer = RequestSerializer(requests)
            return Response(serializer.data)
    else:
        return Response({'response':"You don't have permission."})
   
    
    if logger.role == 'Admin':
        if request.method == 'PUT':
            serializer = RequestSerializer(requests,data=request.data)
            data={}
            if serializer.is_valid():
                serializer.save()
                data['success'] = 'Updated Successfully'
                return Response(data=data)
            return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'response':"You don't have permission."})
    
    if logger.role == 'Admin':
        if request.method == 'DELETE':
            operation = requests.delete()
            data = {}
            if operation:
                data['success'] = 'Deleted Done'
            else:
                data['failure'] = 'Failed'
            return Response(data=data)
    else:
        return Response({'response':"You don't have permission."})

