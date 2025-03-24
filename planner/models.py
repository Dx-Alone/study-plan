from django.db import models

# Create your models here.

class Phase(models.Model):
    number = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    date_range = models.CharField(max_length=100)
    
    class Meta:
        ordering = ['number']
    
    def __str__(self):
        return f"阶段{self.number}: {self.name}"

class Subject(models.Model):
    phase = models.ForeignKey(Phase, related_name='subjects', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.phase} - {self.name}"

class Task(models.Model):
    subject = models.ForeignKey(Subject, related_name='tasks', on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    
    def __str__(self):
        return self.description

class Note(models.Model):
    phase = models.ForeignKey(Phase, related_name='notes', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Note for {self.phase} at {self.created_at}"
