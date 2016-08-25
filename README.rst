django-sequential-pagination
============================

Paginate ordered Django querysets sequentially with "Next" button. Fully compatible with `django-el-pagination`_ (but doesn't depend on it).

.. _django-el-pagination: https://github.com/shtalinberg/django-el-pagination

Unlike "normal" pagination with ``?page=1``, ``?page=2``, etc., this library:

* Works extremely fast even on huge data sets. For example, on Postgres "normal" pagination takes seconds (or even minutes) on queries like ``?page=1000000``.

* Prevents duplicates on next page if new data was injected at top and shifted page boundaries (this is especially important for AJAX pagination).


Installation
============

::

        pip install django-sequential-pagination


Usage
=====

Add ``django_sequential_pagination`` to ``INSTALLED_APPS``:

.. code:: python

	# settings.py

	INSTALLED_APPS = [
		...
		'django_sequential_pagination',
	]


Pass an *ordered* queryset to the template:

.. code:: python

	# views.py
	
	def view_posts(request):
		return render(request, "blog/posts.html", {
			'posts': Post.objects.all().order_by('-time', '-id'),
		})


Make sure that the ordering always has a tie breaker as the last key, otherwise you may get duplicates on page boundaries.

Now, paginate objects in the template:

.. code:: django

	{% load pagination %}

	{% paginate posts per_page=10 as page %}

	{% for post in page.objects %}
		<div>Post #{{ post.id }}</div>
	{% endfor %}

	{% if page.next_page_url %}
		<a href="{{ page.next_page_url }}">Next</a>
	{% endif %}


Settings
--------

You can override the default settings in your ``settings.py``:

.. code:: python

	SEQUENTIAL_PAGINATION_PER_PAGE = 20
	SEQUENTIAL_PAGINATION_KEY = 'from'  # querystring key to use, as in ?from=XXXX


django-el-pagination
--------------------

You can enable endless pagination with `django-el-pagination`_ by putting this in the page template:

.. _django-el-pagination: https://github.com/shtalinberg/django-el-pagination

.. code:: django

	{% paginate posts per_page=10 key='page' as page %}

	{% for post in page.objects %}
		<div>Post #{{ post.id }}</div>
	{% endfor %}

	{% if page.next_page_url %}
		<nav class="endless_container">
			<ul class="pagination"><!-- Bootstrap v3 styles -->
				<li>
					<a class="endless_more" href="{{ page.next_page_url }}" rel="{{ page.key }}">Show more</a>
				</li>
			</ul>
		</nav>
	{% endif %}

	<script>
		$.endlessPaginate({paginateOnScroll: true});
	</script>


Make sure the pagination ``key`` (or ``SEQUENTIAL_PAGINATION_KEY``) matches your ``AjaxListView.key``. The defaults are different (``from`` and ``page``, respectively).


Jinja2
------

If Jinja2 is installed, ``django_sequential_pagination.templatetags.pagination`` will be a ``jinja2.contextfunction``.

Additionally, if `django_jinja`_ is installed, it will be registered automatically as a template tag, so you can use it right away:

.. _django_jinja: https://github.com/niwinz/django-jinja

.. code:: jinja

	{% set page = paginate(posts, per_page=10) %}

	{% for post in page.objects %}
		<div>Post #{{ post.id }}</div>
	{% endfor %}

	{% if page.next_page_url %}
		<a href="{{ page.next_page_url }}">Next</a>
	{% endif %}
