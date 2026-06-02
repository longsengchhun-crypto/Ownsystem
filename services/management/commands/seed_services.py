from django.core.management.base import BaseCommand
from django.utils.text import slugify
from services.models import Service

class Command(BaseCommand):
    help = 'Seeds the database with predefined creative media services'

    def handle(self, *args, **options):
        services_data = [
            {
                'name': 'Video Editing / Shooting',
                'description': 'Professional cinematic video capture and post-production editing including commercial, corporate, and event videography with color correction, sound mixing, and cuts using industry-standard equipment.',
                'starting_price': 250.00
            },
            {
                'name': 'Poster Design',
                'description': 'High-impact poster and banner designs for events, promotions, and marketing campaigns with stunning visuals that communicate your message powerfully.',
                'starting_price': 50.00
            },
            {
                'name': 'VFX',
                'description': 'Visual Effects production including compositing, motion tracking, green screen keying, particle effects, and cinematic CGI elements to elevate your video content.',
                'starting_price': 300.00
            },
            {
                'name': 'Product 3D Modeling',
                'description': 'Photorealistic 3D modeling, texturing, and rendering of products for e-commerce, advertisements, and presentations that showcase every detail of your product.',
                'starting_price': 400.00
            },
            {
                'name': 'Promotion Video Creation',
                'description': 'End-to-end promotional video production — from script and storyboard to filming and editing — designed to capture attention and convert viewers into customers.',
                'starting_price': 500.00
            },
            {
                'name': 'Event Photo/Video Shooting',
                'description': 'Full-coverage professional photography and videography for corporate events, weddings, product launches, concerts, and special occasions with same-day previews.',
                'starting_price': 350.00
            },
        ]

        for s in services_data:
            slug = slugify(s['name'])
            service, created = Service.objects.update_or_create(
                slug=slug,
                defaults={
                    'name': s['name'],
                    'description': s['description'],
                    'starting_price': s['starting_price'],
                    'active': True
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created service: {s['name']}"))
            else:
                self.stdout.write(self.style.WARNING(f"Updated service: {s['name']}"))
