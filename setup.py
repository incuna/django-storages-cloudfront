from setuptools import setup, find_packages

setup(
    name = "django-storages-cloudfront",
    packages = find_packages(),
    include_package_data=True,
    install_requires=[
        "django-storages",
    ],
    version = "0.1",
    description = "Extend django-storages storages.backends.s3.S3Storage to use a Amazone CloudFront domain for urls.",
    author = "Incuna Ltd",
    author_email = "admin@incuna.com",
    url = "http://incuna.com/",
)
