from django.core.management.base import BaseCommand
from django.db.models import get_models


class Command(BaseCommand):
    """List of all models with counting of objects in each of them"""
    def handle(self, *args, **options):
        """command's handle method"""
        counted_models = {len(model.objects.all()): model
                          for model in get_models()}

        self.stdout.write(
            'LIST OF ALL MODELS WITH COUNTING OF OBJECTS IN EACH OF THEM')
        for count, model in counted_models.iteritems():
            output = '%s: %s objects' % (model._meta.module_name, count)
            self.stdout.write(output)

        self.stderr.write(
            'LIST OF ALL MODELS WITH COUNTING OF OBJECTS IN EACH OF THEM')
        for count, model in counted_models.iteritems():
            output = '%s: %s objects' % (model._meta.module_name, count)
            self.stderr.write('error: ' + output)
