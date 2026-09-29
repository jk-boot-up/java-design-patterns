# Dependencies

This project uses Spring Boot and Spring Security, which the plain Java
version of Token Authentication does not. Skipping it loses none of the
pattern: the plain version teaches all of it with nothing installed.

## What Spring Boot is

Spring Boot starts a Java web server from your classes; here, several instances in one program, each on a free local port.

## What Spring Security is

Spring Security is a set of filters that run before your controllers. httpBasic accepts a user name and password for signing in. oauth2ResourceServer with jwt expects a Bearer token on every request and checks it with a JwtDecoder. A JwtEncoder signs new tokens. Validators decide whether a decoded token is acceptable: JwtTimestampValidator checks expiry, and you can add your own, as the revoked list does.

## What JSON Web Tokens and Nimbus is

A JWT has three parts, header, payload and signature, joined by dots. Nimbus JOSE + JWT is the library Spring Security uses to sign and check them; HS256 signs with a shared secret.

## Why this project uses them

The plain version builds the token by hand. This version shows how most Java
services really do it: a framework that checks every request before your code
runs.

## What to install

Only a JDK, version 21. Gradle downloads the rest, and the versions are pinned:

| Tool | Version |
| --- | --- |
| Java | 21 |
| Spring Boot (webmvc, security, oauth2 resource server starters) | 4.1.1 |

## What it costs

- A framework and its configuration to learn.
- Several seconds to start each Spring Boot instance.
