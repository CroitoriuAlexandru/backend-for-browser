import os

if os.environ.get("DJANGO_ENV") == "PRODUCTION":
    print("Production settings loaded")
    from .production_settings import *
else:
    print("Local settings loaded")
    from .local_settings import *