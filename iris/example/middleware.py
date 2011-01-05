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
            def rewrite_url(url, always=False):
                if always or '://' not in url:
                    hashbits = url.split('#', 1)
                    bits = hashbits.pop(0).split('?', 1)
                    url = bits.pop(0)
                    url += '?u={0}'.format(override_user)
                    if bits:
                        url = '{0}&{1}'.format(url, bits[0])
                    if hashbits:
                        url = '{0}#{1}'.format(url, hashbits[0])
                return url
            if response.status_code == 200:
                doc = pq(response.content, parser='html')
                # Replace hrefs in 'a' tags.
                for a in doc('a'):
                    url = a.attrib.get('href')
                    if url:
                        a.attrib['href'] = rewrite_url(url)
                # Replace actions in 'form' tags.
                for form in doc('form'):
                    url = form.attrib.get('action')
                    if url:
                        form.attrib['action'] = rewrite_url(url)
                # Add a header.
                header = pq('<div class="override-user"></div>').text(override_user)
                header.prependTo(doc('html'))
                # Add a title.
                title = doc('title')
                title.text('[{0}] {1}'.format(override_user, title.text()))
                response.content = '<!DOCTYPE html>' + doc.__html__()
            elif response.status_code == 302:
                response['Location'] = rewrite_url(response['Location'], always=True)
        return response
