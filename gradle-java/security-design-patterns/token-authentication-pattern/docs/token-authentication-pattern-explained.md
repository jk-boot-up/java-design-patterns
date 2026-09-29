# Token Authentication, Explained

## The pattern in one sentence

Token Authentication gives the client a signed statement of who it is and
until when, which any server with the key can check on its own.

## The 5 acts

### 1. Sessions on one server

Ana signs in on server A, which remembers ana under a session identifier in
its own memory. The next request, sent to A, shows ana's cart. But when the
load balancer sends a request to server B, B has never heard of that session
and replies 401, please sign in.

### 2. A signed token

Now signing in returns a token. Its payload says the customer is ana and
when the token expires, fifteen minutes later, and it carries a signature
made with the shop's secret key. Both servers hold the key, so both check the
signature themselves and show Ana's cart. There is no shared session store.

### 3. Forged and expired

Someone edits the payload to say ben instead of ana. The signature no longer
matches the payload, and the server refuses it: bad signature. And the
genuine token, used after its fifteen minutes, is refused as expired.

### 4. Signing out early

Ana signs out, but the token itself still says it is valid for fifteen
minutes, so a server accepts it. Server A adds the token's identifier to a
revoked list and refuses it. But server B keeps its own list and still
accepts it. The answer is short-lived tokens, and a revoked list shared by
every server.

### 5. The bill

The payload is only encoded, not encrypted: anyone who sees the token can read
it, so it must never hold secrets. And everything rests on the key: whoever
steals it can sign a token for any customer. Keep it in a secrets manager,
and rotate it.

## The verdict

Use tokens when several servers or services must recognise the same customer.
Keep them short-lived, put nothing secret in the payload, guard and rotate the
key, and plan for early sign-out.

## How to recognise this in code you did not write

- `Authorization: Bearer eyJ...` headers.
- Three dot-separated base64 parts.
- Claims named `sub`, `exp` and `jti`.

## Where you have already met this

- JWTs in `Authorization: Bearer` headers.
- OAuth 2.0 access tokens and OpenID Connect ID tokens.
- Spring Security's resource-server support and libraries such as jjwt and Nimbus.
