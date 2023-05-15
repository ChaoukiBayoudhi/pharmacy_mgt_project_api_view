from django.shortcuts import render
from rest_framework.decorators import api_view

from pharmacy_app.models import Doctor, Prescription
from pharmacy_app.serializers import DoctorSerializer, PatientSerializer
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
    #if the request is sending using the HTTP GET method
    #=>return all the doctors in JSON format
    if request.method=='GET':
        doctors=Doctor.objects.all()
        #convert the doctors queryset to json format
        #the many parameter is set to True because we are serializing many objects
        serializer=DoctorSerializer(doctors,many=True)
        #JsonResponse is a subclass of HttpResponse is used to return JSON data
        #the first parameter is the data to be returned
        #the second parameter is the HTTP status code : like 201,400,404,500,202, ...
        #there is other classes like JsonResponse like HttpResponse,FileResponse,StreamingHttpResponse, Response
        #the Response class is used to return data in other formats like XML,HTML,JSON, ...
        return JsonResponse(serializer.data,status=status.HTTP_200_OK)
    elif request.method=='POST':
        #request.data =>to get the data sent by the user in the HTTP request body
        #convert the json data to python object
        x=request.data
        doctor=DoctorSerializer(data=x)
        #verify if passed data is valid
        #the data is not valid if for example the email is not well formatted(abc.xyz@fdgfhg)
        if doctor.is_valid():
            #add the doctor to the database
            doctor.save()
            #return the added doctor to the user with status 201
            #the data is returned in json format
            #the first parameter is the data to be returned
            #the second parameter is the HTTP status code : like 201,400,404,500,202, ...
            return JsonResponse(doctor.data,status=status.HTTP_201_CREATED)
        #if the data is not valid return the errors detected by the serializer to the user with status 400
        return JsonResponse(doctor.errors,status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({'message':'You have to use POST or GET'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
@api_view(['GET','DELETE'])
#this function get all doctor patients or delete all of them
def get_doctor_patients(request,doctor_id):
    
        doctor1=Doctor.objects.get(pk=doctor_id)
        if doctor1 is None:
            return JsonResponse({'message':f'Doctor with id = {doctor_id} not found'},status=status.HTTP_404_NOT_FOUND)

        patients=Prescription.objects.filter(doctor=doctor1)
        if request.method=='GET':
            serializer=PatientSerializer(patients,many=True)
            #serializer.data allows to get the data in json format after serialization
            return JsonResponse(serializer.data,status=status.HTTP_200_OK)
        elif request.method=='DELETE':
            for patient in patients:
                patient.delete()
            return JsonResponse({'message':f'All patients of doctor with id = {doctor_id} are deleted'},status=status.HTTP_202_ACCEPTED)
        return JsonResponse({'message':'You have to use GET or DELETE'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        