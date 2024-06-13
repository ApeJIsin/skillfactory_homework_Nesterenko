from django.core.management.base import BaseCommand, CommandError
from NewsPaper.news.models import Post, Category


class Command(BaseCommand):
    help = 'Delete all posts in the selected category'
    missing_args_message = 'Required arguments missing'
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        answer = input(f'Do you really want to delete all posts from category {options["category"]}? yes/no\n')

        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Cancelled'))
            return
        try:
            category = Category.objects.get(name=options["category"])
            Post.objects.filter(category=category).delete()
            self.stdout.write(self.style.SUCCESS(
                f'Succesfully deleted all posts from category {options["category"]}'))  # в случае неправильного подтверждения говорим, что в доступе отказано
        except Post.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Could not find category {options["category"]}'))