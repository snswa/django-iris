from django.contrib.auth.models import User
from pyquery import PyQuery as pq


class OverrideUserMiddleware(object):
    """
    Provide a way to quickly test views with a variety of users in the
    same browser session.

    Just set `u` to ``alice``, ``bob``, or ``carla`` in the URL, e.g.::

        http://localhost:8000/iris/?u=carla
    """

    def process_view(self, request, view_func, view_args, view_kwargs):
        override_user = request.GET.get('u')
        if override_user:
            request.user = User.objects.get(username=override_user)

    def process_response(self, request, response):
        """Rewrite relative URLs in http responses to include user override."""
        override_user = request.GET.get('u')
        if override_user:
            if response.status_code == 200:
                doc = pq(response.content, parser='html')
                # Replace hrefs in 'a' tags.
                for a in doc('a'):
                    href = a.attrib.get('href')
                    if href and '://' not in href:
                        delim = '&' if '?' in href else '?'
                        a.attrib['href'] = '{0}{1}u={2}'.format(href, delim, override_user)
                # Replace actions in 'form' tags.
                for form in doc('form'):
                    action = form.attrib.get('action')
                    if action and '://' not in action:
                        delim = '&' if '?' in action else '?'
                        form.attrib['action'] = '{0}{1}u={2}'.format(action, delim, override_user)
                # Add a header.
                header = pq('<div class="override-user"></div>').text(override_user)
                header.prependTo(doc('html'))
                # Add a title.
                title = doc('title')
                title.text('[{0}] {1}'.format(override_user, title.text()))
                response.content = '<!DOCTYPE html>' + doc.__html__()
            elif response.status_code == 302:
                location = response['Location']
                delim = '&' if '?' in location else '?'
                response['Location'] = '{0}{1}u={2}'.format(location, delim, override_user)
        return response
