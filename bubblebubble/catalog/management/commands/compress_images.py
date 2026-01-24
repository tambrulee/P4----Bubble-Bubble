from django.core.management.base import BaseCommand
from django.conf import settings
from PIL import Image
from pathlib import Path


class Command(BaseCommand):
    help = "Quick-compress product images to WebP for Lighthouse"

    def handle(self, *args, **kwargs):
        media_root = Path(settings.MEDIA_ROOT) / "products"

        if not media_root.exists():
            self.stdout.write(self.style.ERROR(f"{media_root} not found"))
            return

        for img_path in media_root.glob("*"):
            if img_path.suffix.lower() not in [".jpg", ".jpeg", ".png", ".webp"]:
                continue

            img = Image.open(img_path)

            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            img.thumbnail((1200, 1200), Image.LANCZOS)

            img.save(
                img_path,
                format="WEBP",
                quality=75,
                method=6
            )

            self.stdout.write(f"Compressed {img_path.name}")
