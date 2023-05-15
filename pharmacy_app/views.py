from django.shortcuts import render
from rest_framework.decorators import api_view

from pharmacy_app.models import Doctor
from pharmacy_app.serializers import DoctorSerializer
from rest_framework.response import JsonResponse
from rest_framework import status
# Create your views here.
#this function gets all the doctors from the database
#or add a new doctor to the database
#we have one url for both operations
#url=http://localhost:8000/api/doctor/
#if you use GET method you will get all the doctors
#if you use POST method you will add a new doctor
@api_view(['GET','POST'])
def get_add_doctor(request):
    if request.method=='GET':
        doctors=Doctor.objects.all()
        serializer=DoctorSerializer(doctors,many=True)
        return JsonResponse(serializer.data,status=status.HTTP_200_OK)
    elif request.method=='POST':
        #convert the json data to python object
        serializer=DoctorSerializer(data=request.data)
        #verify if passed data is valid
        #ithe data is not valid if for example the email is not well formatted(abc.xyz@fdgfhg)
        if serializer.is_valid():
            #add the doctor to the database
            serializer.save()
            #return the added doctor to the user with status 201
            #the data is returned in json format
            return JsonResponse(serializer.data,status=status.HTTP_201_CREATED)
        #if the data is not valid return the errors detected by the serializer to the user with status 400
        return JsonResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({'message':'You have to use POST or GET'},status=status.HTTP_405_METHOD_NOT_ALLOWED)

