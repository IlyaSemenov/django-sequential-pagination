from django.conf import settings

PER_PAGE = 20
KEY = 'from'

__all__ = ['PER_PAGE', 'KEY']

for f in __all__:
	v = getattr(settings, 'SEQUENTIAL_PAGINATION_' + f, None)
	if v is not None:
		globals()[f] = v
