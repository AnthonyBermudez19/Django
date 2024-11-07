from django.db import models

# Create your models here.
class Ticket(models.Model):
    id = models.AutoField(primary_key=True)
    nombre=models.CharField(max_length=50)
    apellido=models.CharField(max_length=50)
    dni=models.CharField(max_length=10)
    priority = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.nombre} - {self.apellido}- {self.dni} - Priority: {self.priority}"

class TicketAtendido(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    dni = models.CharField(max_length=10)
    priority = models.IntegerField(default=0)
    atendido_en = models.DateTimeField(auto_now_add=True)  # Fecha y hora de atención

    def __str__(self):
        return f"Atendido: {self.nombre} {self.apellido} - {self.atendido_en}"


