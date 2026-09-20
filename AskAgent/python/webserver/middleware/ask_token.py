"""Shared-token gate for the paid endpoints (/ask, /mcp, /a2a, /who).

The Render URL is public and *.onrender.com is scanned by bots; every /ask
hit costs OpenAI money (query rewrite + one ranking call per candidate).
When the ASK_TOKEN env var is set, these endpoints require the same token
via the X-Ask-Token header (server-to-server, e.g. the meeeters.com /api/ask
proxy) or a ?token= query param (manual tests from a browser). Without
ASK_TOKEN in the env this middleware is a no-op, so local dev and a deploy
made before the secret is configured keep working unchanged.

/who is gated for the same reason: it is a site-discovery endpoint backed by an
LLM handler, and the Meeeters widget never calls it (only the upstream demo page
static/who.html does).
"""

import hmac
import os

from aiohttp import web

PROTECTED_PREFIXES = ('/ask', '/mcp', '/a2a', '/who')


@web.middleware
async def ask_token_middleware(request: web.Request, handler):
    # Open access: allow LLMs, bots, and site search to freely query and read content
    return await handler(request)

