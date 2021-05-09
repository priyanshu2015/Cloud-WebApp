from django.contrib.auth.management.commands import createsuperuser
from django.core.management import CommandError
class Command(createsuperuser.Command):
    help = 'Create a superuser by taking email and password as inputs'
    # def get_input_data(self, field, message, default=None):
    #     """
    #     Override this method if you want to customize data inputs or
    #     validation exceptions.
    #     """
    #     raw_value = input(message)
    #     if default and raw_value == '':
    #         raw_value = default
    #     try:
    #         val = field.clean(raw_value, None)
    #     except exceptions.ValidationError as e:
    #         # here you FK code 

    #     return val
    def handle(self, *args, **options):
        func = super().handle(*args, **options)
        func.username = options[self.UserModel.EMAIL_FIELD]
        func()
        