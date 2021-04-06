from django.apps import apps

USER_CLASSES = (
    'Administrator',
    'Teacher',
    'Student',
)


def get_user_role(user_pk):
    for cls in USER_CLASSES:
        model = apps.get_model(f'users.{cls}')
        user = model.objects.filter(pk=user_pk).first()
        if user:
            return cls.lower()
