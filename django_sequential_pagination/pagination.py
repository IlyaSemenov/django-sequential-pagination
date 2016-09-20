from django.db.models import Q

from .settings import PER_PAGE, KEY


class Order:
	def __init__(self, str_order):
		if str_order[0] == '-':
			self.key = str_order[1:]
			self.reverse = True
		else:
			self.key = str_order
			self.reverse = False

	@property
	def asc(self):
		return not self.reverse

	@property
	def desc(self):
		return self.reverse


def format_qs_value(v):
	# None: -
	# -: --
	# -5: -5
	# --: ---
	# ---: ----
	if v is None:
		return '-'
	elif isinstance(v, bool):
		v = int(v)
	s = str(v)
	if s == '-' or s.startswith('--'):
		return '-' + s
	else:
		return s


def parse_qs_value(s):
	if s == '-':
		return None
	elif s.startswith('--'):
		return s[1:]
	else:
		return s


def paginate(request, objects, per_page=PER_PAGE, key=KEY, use_offset=False):
	if isinstance(object, list):
		return objects

	if use_offset:
		order_by = None
	else:
		order_by = objects.query.order_by or (hasattr(objects, 'model') and objects.model._meta.ordering) or None

	if order_by:
		orders = [Order(order_key) for order_key in order_by]
		page_from = [parse_qs_value(v) for v in request.GET.getlist(key) or request.POST.getlist(key)]
		objects = filter_objects(objects, orders, page_from)
		offset = 0
	else:
		# Fallback to OFFSET pagination
		try:
			offset = int(request.GET.get(key) or request.POST.get(key))
		except (TypeError, ValueError):
			offset = 0
		page_from = [offset]

	objects = objects[offset:offset+per_page+1]  # Extend range to include the first record of the next page
	objects = list(objects)

	if len(objects) > per_page:
		next_object = objects[-1]
		objects = objects[:per_page]
		next_get = request.GET.copy()
		if order_by:
			next_get.setlist(key, [format_qs_value(getattr(next_object, order.key)) for order in orders])
		else:
			next_get[key] = str(offset + per_page)
		next_page_url = '?' + next_get.urlencode()
	else:
		next_page_url = None

	return {
		'objects': objects,
		'next_page_url': next_page_url,
		'key': key,
		'from': page_from,
	}


def filter_objects(objects, orders, page_from):
	q = Q()
	prev_q = Q()
	for order, from_v in zip(orders, page_from):
		if order.asc:
			if from_v:
				# 1 2 (v=3) 4 5 NULL NULL
				this_q = Q(**{'{0}__gte'.format(order.key): from_v}) | Q(**{order.key: None})
			else:
				# 1 2 3 (v=NULL) NULL
				this_q = Q(**{order.key: None})
		else:
			if from_v:
				# NULL NULL 5 4 (v=3) 2 1
				this_q = Q(**{'{0}__lte'.format(order.key): from_v})
			else:
				# (v=NULL) NULL 3 2 1
				this_q = None  # Don't filter, we only started and need all of them. Rely on other keys!

		if this_q:
			if prev_q:
				# TODO: optimize
				q &= (prev_q & this_q) | ~prev_q
			else:
				q &= this_q
		prev_q &= Q(**{order.key: from_v})

	return objects.filter(q)
