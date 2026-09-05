# Publishing API

The public post field is `caption`; `body` is an internal persistence name.
`scheduled_at` accepts ISO 8601 with an offset and denotes an instant, not a wall
clock value to reinterpret.

`GET /api/posts/` returns only workspaces of the authenticated member.
`POST /api/posts/{id}/schedule/` may schedule approved posts only.

Each `ChannelConnection` owns its credential. The global sandbox token is for
health checks and must never replace a workspace credential on publish calls.
