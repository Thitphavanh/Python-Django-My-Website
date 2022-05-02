# custom_tags.py - {% load custom_tags %}

from django import template
from ..models import Allproduct, Catagory

register = template.Library()


@register.simple_tag
def hello_tag():  # {% hello_tag %}
    return '<----Hello Tag---->'


@register.simple_tag
def show_allproduct():
    count = Allproduct.objects.count()
    return count


@register.inclusion_tag('myapp/allcatagory.html')
def all_catagory():
    catagorys = Catagory.objects.all()
    return {'allcatagorys': catagorys}
