from django import template

register = template.Library()


@register.filter(name="snake_to_title")
def snake_to_title(value):
    """Convert snake_case to Title Case."""
    if not isinstance(value, str):
        return value
    return value.replace("_", " ").title()
