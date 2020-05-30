from .models import ModelActionLog
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete


ignored_models = ['ModelActionLog', 'LogEntry', 'ContentType']


@receiver(post_save, dispatch_uid='nope')
def post_save_signal(sender, instance, created, dispatch_uid='nope', **kwargs):
    if created and sender.__name__ not in ignored_models:
        ModelActionLog.objects.create(
            model_name=sender.__name__, instance=instance, action='create')
    elif not created and sender.__name__ not in ignored_models:
        ModelActionLog.objects.create(
            model_name=sender.__name__, instance=instance, action='update')


@receiver(post_delete, dispatch_uid='nope')
def post_delete_signal(sender, instance, dispatch_uid='nope', **kwargs):
    if sender.__name__ not in ignored_models:
        ModelActionLog.objects.create(
            model_name=sender.__name__, instance=instance, action='delete')
