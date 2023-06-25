from django.db import models

# Create your models here.
class Question(models.Model):
    TYPE_CHOICES = (
        ('WAIT_ANSWER', 'Ждать ответа'),
        ('OFFER_OPTIONS', 'Предлагать варианты'),
    )
    text = models.CharField(verbose_name='Текст вопроса', blank=False, null=False, max_length=1000)
    question_type = models.CharField(verbose_name='Тип ответов', max_length=50, choices=TYPE_CHOICES)
    need_one_answer = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f'Вопрос: {self.text}'

    @property
    def question_dict(self):
        result = {
            'text': self.text,
            'type': self.question_type,
            'many_variants': self.need_one_answer,
            'variants': Variant.variants_dict(self)
        }
        return result


class Variant(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос')
    value = models.CharField(verbose_name='Ответ', blank=False, null=False, max_length=500)
    is_true = models.BooleanField(verbose_name='Правильный ответ', default=False)

    @classmethod
    def variants_dict(self, question: Question):
        variants = Variant.objects.filter(question=question)
        result = [
            {'value': v.value, 'is_true': v.is_true}
            for v in variants
        ]
        return result


class Probationer(models.Model):
    user_name = models.CharField('User name', max_length=150)
    user_id = models.BigIntegerField('Telegram id', null=False, blank=False,)
    end_time = models.IntegerField('Time to goodbye', null=False, blank=False,)
    answers = models.TextField('True variants', null=False, blank=False,)
    success = models.BooleanField('Success guess?', null=True, default=None) # None - timeout, True - good, False - fail
    actual = models.BooleanField('Actual event?', default=True)
    created_at = models.DateTimeField('Time of event', auto_now_add=True)