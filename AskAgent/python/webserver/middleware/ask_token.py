"""Shared-token gate for the paid endpoints (/ask, /mcp, /a2a).

The Render URL is public and *.onrender.com is scanned by bots; every /ask
hit costs OpenAI money (query rewrite + one ranking call per candidate).
When the ASK_TOKEN env var is set, these endpoints require the same token
via the X-Ask-Token header (server-to-server, e.g. the meeeters.com /api/ask
proxy) or a ?token= query param (manual tests from a browser). Without
ASK_TOKEN in the env this middleware is a no-op, so local dev and a deploy
made before the secret is configured keep working unchanged.
"""

import hmac
import os

from aiohttp import web

PROTECTED_PREFIXES = ('/ask', '/mcp', '/a2a')


@web.middleware
async def ask_token_middleware(request: web.Request, handler):
    expected = os.environ.get('ASK_TOKEN', '')
    if (
        not expected
        or request.method == 'OPTIONS'  # never block CORS preflight
        or not request.path.startswith(PROTECTED_PREFIXES)
    ):
        return await handler(request)

    supplied = request.headers.get('X-Ask-Token') or request.query.get('token', '')
    if not hmac.compare_digest(supplied.encode(), expected.encode()):
        return web.json_response(
            {'error': 'Missing or invalid token', 'type': 'auth_required'},
            status=401,
        )
    return await handler(request)
