from django.apps import AppConfig


class ObjectDetectionConfig(AppConfig):
    verbose_name = "Загруженные изображения"
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'object_detection'
