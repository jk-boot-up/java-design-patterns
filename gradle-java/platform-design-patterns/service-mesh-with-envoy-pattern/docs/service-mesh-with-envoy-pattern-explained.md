# Service Mesh with Envoy, Explained

## The pattern in one sentence

With Envoy, the proxy in front of a service applies the retry, identity and counting policy from its configuration, and the service has none of that code.

## What is new here

The pattern is [Service Mesh](../service-mesh-pattern). This page is only what Envoy adds.

### Each Service Carries Its Own

The payment service refuses its first two calls, for each caller in turn. With retry code of three, none, and one tries: checkout worked, refunds failed, reports failed. Three services, three copies of the retry code, three different behaviours.

```
  the payment service refuses its first 2 calls, for each caller in turn. with retry code of 3, 0 and 1 tries: checkout worked, refunds failed, reports failed.
  three services, three copies of the retry code, three different behaviours.
```

### A Proxy Beside The Service

Envoy is told to retry server errors up to three times. The checkout has no retry code, and the call worked. The payment service received three calls, and Envoy counts two retries.

```
  Envoy is told to retry 5xx answers up to 3 times. the checkout has no retry code. the call worked. the payment service received 3 calls, and Envoy counts 2 retries.
```

### Change The Policy Once

One setting in Envoy's configuration is changed, from three retries to none. The same call fails. Services changed or redeployed: none.

```
  one setting in Envoy's configuration changed, from 3 retries to 0. the same call failed. services changed or redeployed: 0.
```

### Who Is Calling

Only checkout and refunds are allowed. Checkout gets a 200. Gift cards gets a 403. The payment service received one call: the proxy turned the other away before it got there. Here the caller's name is a header. A real mesh checks a certificate instead, which a service cannot forge.

```
  only checkout and refunds are allowed. checkout: status 200. gift-cards: status 403.
  the payment service received 1 call. the proxy turned the other one away before it got there.
  here the caller's name is a header. a real mesh checks a certificate instead, which a service cannot forge.
```

### Numbers For Free

Read from Envoy, and not from any service: requests to payments, three; retries, two; retries that ended in success, one. No service counted anything. The proxy did.

```
  read from Envoy, and not from any service: requests to payments 3, retries 2, retries that ended in success 1.
  no service counted anything. the proxy did.
```

### The Bill

One call, with two refusals: the payment service received three calls. Retrying multiplies the load on a service that is already struggling. Every call now crosses a proxy, which is a second process and a second network hop. And the policy is in a configuration file of about forty five lines, that someone must read, and keep right.

```
  one call, with 2 refusals: the payment service received 3 calls. retrying multiplies the load on a service that is already struggling.
  every call now crosses a proxy, which is a second process and a second network hop. this demo needed 1 more container for 1 service.
  and the policy is in a configuration file of about 45 lines, that someone must read, and keep right.
```

## The verdict

Put retries, identity and counting in the proxy, and set them in one place. Keep retries small, since they multiply load. Check identity with certificates, not names. And keep the configuration under review, because it now decides how every call behaves.

## How to recognise this in code you did not write

- `retry_policy` and `num_retries` in Envoy configuration.
- A `/stats` page with `upstream_rq_retry` counters.
- An RBAC filter with principals.
- A sidecar container named `envoy` or `istio-proxy` beside a service.

## Where you have already met this

Istio, Consul Connect, AWS App Mesh, and many gateways and load balancers.

## When this is too much

For a few services, a shared library is simpler. A proxy for each service is more processes to run and understand.
