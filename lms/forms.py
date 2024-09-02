from .models import Course, Lesson
from django import forms


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class CourseForm(forms.ModelForm):
    # lessons = forms.ModelMultipleChoiceField(
    #     queryset=Lesson.objects.all(),
    #     required=False,
    #     widget=forms.CheckboxSelectMultiple,
    #     label='Уроки'
    # )

    class Meta:
        model = Course
        fields = ['title', 'description', 'preview', 'lesson']

    # def save_m2m(self):
    #     print('123')
    #     print(self.instance)
    #     print(self.cleaned_data)
    #     self.instance.lessons.clear()
    #
    #     if self.cleaned_data.get('lessons'):
    #         for lesson in self.cleaned_data['lessons']:
    #             lesson.course = self.instance
    #             lesson.save()

    def save(self, commit=True):
        course = super().save(commit=False)
        print(course)
        print(commit)
        if commit:
            course.save()
            self.save_m2m()
        return course


class LessonForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'description', 'preview', 'video_url', ]
