from django import template

register = template.Library()


@register.filter
def has_tag(tags: str, tag: str) -> bool:
    """
    True if `tag` exists as a whole tag in a comma-separated tags string.
    Handles spaces and case.
    """
    if not tags or not tag:
        return False

    tag = tag.strip().lower()
    parts = [t.strip().lower() for t in tags.split(",") if t.strip()]
    return tag in parts
