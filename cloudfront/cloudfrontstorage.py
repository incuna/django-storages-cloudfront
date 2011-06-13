from django.conf import settings
from storages.backends.s3 import S3Storage, SECURE_URLS, QUERYSTRING_EXPIRE, QUERYSTRING_ACTIVE
from S3 import QueryStringAuthGenerator, CallingFormat

AWS_CLOUDFRONT_DOMAIN = getattr(settings, 'AWS_CLOUDFRONT_DOMAIN', None)

class CouldFrontStorage(S3Storage):

    def __init__(self, *args, **kwargs):
        super(CouldFrontStorage, self).__init__(*args, **kwargs)

        if AWS_CLOUDFRONT_DOMAIN:
            try:
                access_key = args[1]
            except IndexError:
                access_key = kwargs.get('access_key', None)
            try:
                secret_key = args[2]
            except IndexError:
                secret_key = kwargs.get('secret_key', None)

            if not access_key and not secret_key:
                access_key, secret_key = self._get_access_keys()

            if AWS_CLOUDFRONT_DOMAIN:
                self.url_generator = QueryStringAuthGenerator(access_key, secret_key, 
                                                                   is_secure=SECURE_URLS,
                                                                   server=AWS_CLOUDFRONT_DOMAIN,
                                                                   calling_format=CallingFormat.VANITY)
                self.url_generator.set_expires_in(QUERYSTRING_EXPIRE)


    def url(self, name):
       if not AWS_CLOUDFRONT_DOMAIN:
           return super(CouldFrontStorage, self).url(name)

       name = self._clean_name(name)
       if QUERYSTRING_ACTIVE:
           return self.url_generator.generate_url('GET', '', name)
       else:
           return self.url_generator.make_bare_url('', name)

