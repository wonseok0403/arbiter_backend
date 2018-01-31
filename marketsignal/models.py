from django.db import models

# Create your models here.
CARTEGORY_TYPES = (
    ('M','Market'),
    ('S', 'Size'),
    ('St', 'Style'), # 중형주
    ('I', 'Industry'), # 소형주
)


class Index(models.Model):
    date = models.CharField(max_length=8)
    name = models.CharField(max_length=15)
    index = models.FloatField(blank=True, null=True)
    volume = models.IntegerField(blank=True, null=True)
    cartegory = models.CharField(max_length=2,
                                  choices=CARTEGORY_TYPES,
                                  blank=True,
                                  null=True)

    def __str__(self):
        return '{} {}'.format(self.date, self.name)
