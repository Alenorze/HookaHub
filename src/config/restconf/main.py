# Django-Channels configuration file
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis://redis:6379/1", 6379)],
        },
        "ROUTING": "django_channels.routing.application",
    },
}

ASGI_APPLICATION = 'config.asgi.application'
