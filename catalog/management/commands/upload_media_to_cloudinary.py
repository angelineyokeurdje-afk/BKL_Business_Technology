from django.core.management.base import BaseCommand
from django.core.files import File
from catalog.models import Product, SiteSettings
import os


class Command(BaseCommand):
    help = 'Upload existing local media files to Cloudinary by re-saving ImageFields (requires Cloudinary enabled)'

    def handle(self, *args, **options):
        self.stdout.write('Starting upload of Product images...')
        for p in Product.objects.all():
            if p.image and hasattr(p.image, 'path') and os.path.exists(p.image.path):
                self.stdout.write(f'Uploading Product id={p.id} file={p.image.path}')
                with open(p.image.path, 'rb') as f:
                    p.image.save(os.path.basename(p.image.path), File(f), save=True)

        self.stdout.write('Starting upload of SiteSettings hero_image...')
        for s in SiteSettings.objects.all():
            if s.hero_image and hasattr(s.hero_image, 'path') and os.path.exists(s.hero_image.path):
                self.stdout.write(f'Uploading SiteSettings id={s.id} file={s.hero_image.path}')
                with open(s.hero_image.path, 'rb') as f:
                    s.hero_image.save(os.path.basename(s.hero_image.path), File(f), save=True)

        self.stdout.write(self.style.SUCCESS('Upload complete.'))
