from django.apps import AppConfig


class CarWashAppConfig(AppConfig):
    name = 'car_wash_app'

    def ready(self):
        import car_wash_app.signals
