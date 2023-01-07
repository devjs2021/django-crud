from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Task(models.Model):
    titulo = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    dato_completado = models.DateTimeField(null=True, blank=True)
    importante = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    
    def __str__(self):
        return self.titulo + '-- by ' + self.user.username
    
    