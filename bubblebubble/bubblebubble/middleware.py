import re


class MediaCacheControlMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self._media = re.compile(r"^/media/")

    def __call__(self, request):
        response = self.get_response(request)

        if self._media.match(request.path):
            response["Cache-Control"] = "public, max-age=2592000"  # 30 days

        return response
