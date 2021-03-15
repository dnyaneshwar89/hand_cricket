from django.db import models

# Create your models here.
class LeaderBoard(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    score = models.IntegerField()
    class Meta:
        verbose_name_plural = "LeaderBoard"
    def __str__(self):
        return self.name