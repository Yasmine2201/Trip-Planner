from django.db import models


class Notification(models.Model):
    notification_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('core.User', on_delete=models.CASCADE)
    type = models.CharField(max_length=255)  # 3 types : 'invitation', 'budget', 'visit'
    content = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.type} - {self.created_at}'
