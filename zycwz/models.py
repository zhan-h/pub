from django.db import models


# Create your models here.

class Zycwz(models.Model):
    zy_name = models.CharField(max_length=20)
    zy_profession = models.CharField(max_length=20)
    zy_price = models.FloatField()
    zy_work = models.FloatField()

    def __str__(self):
        return self.zy_name

    class Meta:
        db_table = 'zycwz'
        verbose_name = '中药信息'
