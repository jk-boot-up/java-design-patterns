# Session Guide — Token Authentication with Spring Security Pattern

## Learning Objectives

By the end of the session you can:

- Issue a JWT with Spring Security's JwtEncoder.
- Protect endpoints with the resource-server JWT support.
- Add a custom token validator.
- Explain what a shared secret allows, and what stealing it allows.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: Sessions on one server | 7 min |
| 0:17 | Act 2: A token from Spring Security | 7 min |
| 0:24 | Act 3: Forged and expired | 7 min |
| 0:31 | Act 4: Signing out early | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run`. Open `ShopApp.security`: three lines of configuration.
Open `ShopApp.jwtDecoder`: the expiry and revoked-list validators. Compare
act four's two servers.

## Exercises

1. Share the revoked list between instances through a common bean or a database.
2. Switch to an RSA key pair so services can check tokens without being able to sign them.
3. Add a role claim and require it with `hasAuthority` on one endpoint.
