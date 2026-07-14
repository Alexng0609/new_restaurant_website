from django.core.management.base import BaseCommand

from restaurant_site.localization import translate_vi_to_en
from restaurant_site.models import MenuItem, NewsFeed


class Command(BaseCommand):
    help = (
        "Fill empty English description/content fields from Vietnamese. "
        "Names and titles are not translated — they always stay in Vietnamese."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be translated without saving.",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        menu_count = 0
        news_count = 0

        for item in MenuItem.objects.all():
            if item.description_en.strip():
                continue
            translated = translate_vi_to_en(item.description)
            menu_count += 1
            if dry_run:
                self.stdout.write(f"MenuItem description: {item.name}")
            else:
                MenuItem.objects.filter(pk=item.pk).update(description_en=translated)

        for news in NewsFeed.objects.all():
            if news.content_en.strip():
                continue
            translated = translate_vi_to_en(news.content)
            news_count += 1
            if dry_run:
                self.stdout.write(f"NewsFeed content: {news.title}")
            else:
                NewsFeed.objects.filter(pk=news.pk).update(content_en=translated)

        action = "Would translate" if dry_run else "Translated"
        self.stdout.write(
            self.style.SUCCESS(
                f"{action} descriptions for {menu_count} menu items "
                f"and content for {news_count} news posts."
            )
        )
