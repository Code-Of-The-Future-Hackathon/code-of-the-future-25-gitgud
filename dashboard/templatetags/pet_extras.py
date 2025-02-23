from django import template
from datetime import date

register = template.Library()


@register.filter
def calculate_age(dob):
    if not dob:
        return ''
    today = date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return age
