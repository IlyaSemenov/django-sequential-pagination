from django import template

from django_sequential_pagination.pagination import paginate as do_paginate
from django_sequential_pagination.settings import PER_PAGE, KEY

register = template.Library()


@register.simple_tag(takes_context=True)
def paginate(context, objects, per_page=PER_PAGE, key=KEY):
	"""
	{% paginate objects 10 as page %}
	TODO: test this.
	"""
	return do_paginate(context['request'], objects, per_page, key=key)


try:
	import jinja2
except ImportError:
	pass
else:
	jinja2.contextfunction(paginate)

try:
	from django_jinja import library
except ImportError:
	pass
else:
	library.global_function(paginate)
