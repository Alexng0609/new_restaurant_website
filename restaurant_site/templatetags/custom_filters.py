from django import template

register = template.Library()


@register.filter(name="vnd_format")
def vnd_format(value):
    """
    Format a number as Vietnamese currency style:
    50000 -> "50.000"
    1250000 -> "1.250.000"
    """
    try:
        value = int(round(float(value)))
    except (TypeError, ValueError):
        return value

    return f"{value:,}".replace(",", ".")
