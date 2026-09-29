# Plugin, Explained

## The pattern in one sentence

Plugin lets the code ask only for interfaces while a configuration file per
environment names the class for each one, and a single factory creates them.

## The 5 acts

### 1. Choices scattered in code

`ScatteredChoices` has one method per service, each with its own `if` on the
environment name. When "staging" was added, the payment choice treated it
correctly and returned the fake gateway. The email choice only knew "dev", so
staging fell through to the real SMTP emailer and emailed Priya for real.

### 2. Plugins from configuration

Each environment has a file, `plugins-<env>.properties`, mapping an interface
name to a class name. `PluginFactory` reads it and creates the class.
`Checkout` only names `PaymentGateway` and `Emailer`. In dev it receives the
fake gateway and the sandbox emailer; in prod, the real card gateway and SMTP.

### 3. A new environment

Staging is added again, this time as `plugins-staging.properties`: two lines,
fake gateway and sandbox emailer. No Java code changes, and there is no second
place to forget. Priya's email stays in the sandbox inbox.

### 4. Caught at startup

The demo environment's file misspells `SandboxEmailer` as `SandboxEmaler`.
`PluginFactory.check` creates every configured plugin once when the shop
starts, and reports "cannot create ... SandboxEmaler for Emailer", before the
first customer ever reaches checkout.

### 5. The bill

The compiler cannot see the wiring. A misspelt class name compiles and only
fails at startup. And searching the code for usages of `SandboxEmailer` finds
nothing, because it is only named in text files.

## The verdict

Use it when implementations differ between environments or deployments. Keep
all the wiring in one factory, check every plugin at startup, and in a Spring
application use profiles instead of writing your own.

## How to recognise this in code you did not write

- `Class.forName(...)` next to a properties file.
- `META-INF/services` files and `ServiceLoader`.
- Spring profiles and `@Profile`.

## Where you have already met this

- Java's `ServiceLoader` and `META-INF/services` files.
- Spring profiles and `@ConditionalOnProperty`, which choose beans per environment.
- JDBC drivers, logging back ends such as SLF4J bindings, and servlet containers loading web apps.
