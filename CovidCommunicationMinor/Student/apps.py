from django.apps import AppConfig


class StudentConfig(AppConfig):
    name = 'Student'

    def ready(self):
        import Student.signals