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


@register.simple_tag
def querystring(get_params, key, value):
    """
    Return a URL-encoded querystring based on the current GET params,
    replacing/setting `key` to `value`.

    Usage:
      ?{% querystring request.GET 'page' 2 %}
    """
    params = get_params.copy()
    params[key] = value
    return params.urlencode()
