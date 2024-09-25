# from .models import Subscription
# from django.core.mail import send_mail
#
# DEFAULT_FROM_EMAIL = 'sinister.volkov9@yandex.ru'
#
#
# def send_update_mail(course):
#     subs_list = Subscription.objects.filter(course=course)
#     for sub in subs_list:
#         try:
#             send_mail(
#                 'Курс обновился',
#                 f'Курс "{course}" обновился!',
#                 DEFAULT_FROM_EMAIL,
#                 [sub.user.email],
#             )
#         except Exception as e:
#             print(e)
