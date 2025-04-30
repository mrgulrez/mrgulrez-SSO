from django.db import models

class Dashboard(models.Model):
    user_id = models.IntegerField()
    username = models.CharField(max_length=150)
    last_login = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.username}'s Dashboard"

class Task(models.Model):
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title