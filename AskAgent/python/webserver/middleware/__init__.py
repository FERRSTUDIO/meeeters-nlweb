"""Middleware package for aiohttp server"""

from .ask_token import ask_token_middleware
from .auth import auth_middleware
from .cors import cors_middleware
from .error_handler import error_middleware
from .logging_middleware import logging_middleware
from .streaming import streaming_middleware


def setup_middleware(app):
    """Setup all middleware in the correct order"""
    # Note: Middleware is applied in reverse order
    # So the first in this list is the outermost (executes first)
    app.middlewares.append(error_middleware)
    app.middlewares.append(logging_middleware)
    app.middlewares.append(cors_middleware)
    app.middlewares.append(ask_token_middleware)
    app.middlewares.append(auth_middleware)
    app.middlewares.append(streaming_middleware)


__all__ = [
    'ask_token_middleware',
    'auth_middleware',
    'cors_middleware',
    'error_middleware',
    'logging_middleware',
    'setup_middleware',
    'streaming_middleware'
]
