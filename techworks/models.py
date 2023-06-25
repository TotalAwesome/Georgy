from django.db import models

class TechWorkSource(models.Model):
    # tech_work = models.ForeignKey(TechWork)
    name = models.CharField(max_length=30, null=False, default='default')
    url = models.CharField(max_length=255, default='')
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name


class TechWork(models.Model):
    source = models.ForeignKey(TechWorkSource, on_delete=models.CASCADE)
    start_time = models.DateTimeField('Дата начала', null=True)
    end_time = models.DateTimeField('Дата окончания', null=True)
    time_string = models.CharField('Дата публикации', null=True, max_length=300)
    title = models.CharField('Заголовок', max_length=255)
    description = models.TextField('Описание')
    new = models.BooleanField('Новое', default=True)

    def __str__(self) -> str:
        return f'{self.title} ({self.start_time})'