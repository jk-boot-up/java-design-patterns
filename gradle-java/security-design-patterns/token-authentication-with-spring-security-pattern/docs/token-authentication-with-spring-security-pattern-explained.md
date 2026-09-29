# Token Authentication with Spring Security, Explained

## The pattern in one sentence

With Spring Security, token authentication is a resource-server filter that
checks every request's JWT, and an encoder that issues them at sign-in.

## The 5 acts

### 1. Sessions on one server

Two Spring Boot instances of the shop are running. Ana signs in on server A,
which remembers ana in its HTTP session. With the session cookie, server A
shows ana's cart, but server B has no such session and answers 401, please
sign in.

### 2. A token from Spring Security

Ana signs in once, posting a password to `/token`, and gets back a JWT
signed by Spring Security's encoder: its payload names ana and an expiry
fifteen minutes on. Sent as a Bearer header, it is accepted by server A and by
server B, with no shared session store.

### 3. Forged and expired

Someone edits the payload to say ben. Spring Security refuses it before the
shop's code runs: 401, invalid signature. A token that expired two minutes ago
is refused too: 401, Jwt expired. By default Spring allows sixty seconds of
clock difference; this demo sets it to zero.

### 4. Signing out early

Ana signs out on server A, which adds the token's identifier to its revoked
list, checked by one extra validator. Server A now refuses the token: 401,
revoked. Server B, with its own list, still accepts it. Keep tokens
short-lived, and share any revoked list.

### 5. The bill

The payload is only encoded: anyone can read sub equals ana and when it
expires. And everything rests on the secret. A third instance started with
the stolen secret signs a token for ben, and server A answers 200, ben's cart.
Keep the key in a secrets manager, rotate it, and prefer asymmetric keys when
many services only need to check tokens.

## The verdict

Use Spring Security's JWT support whenever several instances or services must
recognise the same customer. Keep tokens short-lived, set clock skew
deliberately, share revocation, and guard or rotate the signing key.

## How to recognise this in code you did not write

- `.oauth2ResourceServer(o -> o.jwt(...))`.
- `JwtEncoder`, `JwtDecoder` and `OAuth2TokenValidator` beans.
- `@AuthenticationPrincipal Jwt jwt` in controllers.

## Where you have already met this

- `oauth2ResourceServer().jwt()` in Spring Security configurations.
- OAuth 2.0 access tokens from Keycloak, Auth0 or Okta.
- `Authorization: Bearer eyJ...` headers in browser developer tools.
