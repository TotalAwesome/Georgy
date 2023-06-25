from statistics import quantiles
from django.contrib import admin
from captcha.models import Question, Variant, Probationer
# Register your models here.

class QuestionAdmin(admin.ModelAdmin):

    class VariantsInline(admin.StackedInline):
        model = Variant
        extra = 1

    list_display = ('id', 'text', 'question_type', 'need_one_answer')
    list_display_links = ('id',)
    list_editable = ('text', 'question_type', 'need_one_answer')
    inlines = (VariantsInline, )


class VariantAdmin(admin.ModelAdmin):
    list_display = ('question', 'value', 'is_true')
    list_editable = ('value', 'is_true')


class ProbationerAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'user_id', 'success', 'actual', 'created_at', 'answers')
    # list_editable = ('value', 'is_true')

admin.site.register(Question, QuestionAdmin)
admin.site.register(Variant, VariantAdmin)
admin.site.register(Probationer, ProbationerAdmin)