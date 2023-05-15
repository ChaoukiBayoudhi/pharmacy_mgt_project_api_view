from django.db import models

# Create your models here.

class Person(models.Model):
    name = models.CharField(max_length=100,default='Patient')
    phone = models.CharField(max_length=100,default='0000000000')
    email = models.EmailField(max_length=100,unique=True)
    description=models.TextField(null=True,blank=True)
    class Meta:
        ordering = ('name',)
        abstract=True
    def __str__(self):
        return self.name
class Patient(Person):
    birthdate = models.DateField(null=True,blank=True)
    class Meta:
        db_table='patients'
    
class Doctor(Person):
    
    specialty = models.CharField(max_length=100,default='Generalist',choices=[('Generalist','Generalist Doctor'),('Dentist','Dentist'),('Surgeon','Surgeon')])
    

    class Meta:
        ordering = ('name','specialty')
        db_table='doctors'
    def __str__(self):
        return self.email



class Pharmacist(Person):
    birthdate = models.DateField(null=True,blank=True)
    start_working_hour = models.TimeField(default='08:00:00')

    class Meta:
        db_table='pharmacists'
    

class Prescription(models.Model):
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,null=True,blank=True)
    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE,related_name='doctor_prescriptions',null=True,blank=True)
    pharmacist = models.ForeignKey(Pharmacist,on_delete=models.CASCADE,null=True,blank=True)
    date = models.DateField(auto_now_add=True)
    notes = models.TextField(null=True,blank=True)
    class Meta:
        ordering = ('-date',)
        db_table='prescriptions'
    def __str__(self):
        return self.patient.name + ' - ' + self.doctor.name + ' - ' + str(self.date)

class Drug(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    stock=models.PositiveIntegerField(default=0)
    prescription_drugs=models.ManyToManyField(Prescription,through='DrugsPrescription',through_fields=('drug','prescription'))
    class Meta:
        ordering = ('name','-price')
        db_table='drugs'
    def __str__(self):
        return self.name
#implementation of the association class between drug and prescription
class DrugsPrescription(models.Model):
    prescription = models.ForeignKey(Prescription,on_delete=models.CASCADE)
    drug = models.ForeignKey(Drug,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    consuming_duration=models.DurationField(null=True,blank=True)

    class Meta:
        ordering = ('prescription','drug')
        db_table='drugs_prescriptions'

    def __str__(self):
        return self.prescription.patient.name + ' - ' + self.drug.name + ' - ' + str(self.quantity)
    