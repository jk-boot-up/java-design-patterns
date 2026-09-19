# Service Mesh, Explained

## The pattern in one sentence

A service mesh puts a proxy beside every service, and lets the proxies handle retries, identity and measurement for all calls, under one policy that is set in one place.

## The six acts

### Each Service Carries Its Own

The payment service refuses its first two calls. Checkout retries three times, and succeeds. Refunds never retries, and fails. Reports retries once, and fails. Three services, three copies of the retry code, three different behaviours.

```
  the payment service refuses its first 2 calls. checkout retries 3 times: true. refunds never retries: false. reports retries once: false.
  three services, three copies of the retry code, three different behaviours.
```

### A Proxy Beside Each Service

The same bad day, and the same policy for everyone. The call worked. The proxy made three attempts, and the checkout service has no retry code at all.

```
  the same bad day, the same policy for everyone: the call worked, attempts made by the proxy: [checkout->payments calls 1, failed 0, attempts 3].
  the checkout service has no retry code at all.
```

### Change The Policy Once

With three retries, the call works. One setting changed to zero, and it fails. Every service's calls changed. Services redeployed: none.

```
  retries 3: true. one setting changed to 0: false.
  every service's calls changed. services redeployed: 0.
```

### Who Is Calling

Checkout calls payments, and it works. An unknown service calls payments, and is refused. The payment service received one call. The proxy turned the other away before it got there. Denied: one.

```
  checkout calls payments: true. an unknown service calls payments: false.
  the payment service received 1 call. the proxy turned the other one away before it got there. denied: 1.
```

### Numbers For Free

Checkout to payments: two calls, none failed, four attempts. Refunds to payments: one call, none failed, one attempt. No service counted anything. The proxies did.

```
  checkout->payments calls 2, failed 0, attempts 4.
  refunds->payments calls 1, failed 0, attempts 1.
  no service counted anything. the proxies did.
```

### The Bill

One call, with two refusals: the payment service received three calls. Retrying multiplies the load on a service that is already struggling. One attempt takes three ticks through the proxies, and one directly. This call took nine ticks. And three services means three more processes to run, upgrade and understand.

```
  one call, with 2 refusals: the payment service received 3 calls. retrying multiplies the load on a service that is already struggling.
  one attempt takes 3 ticks through the proxies, and 1 directly. this call took 9 ticks.
  and 3 services means 3 more processes to run, upgrade and understand.
```

## The verdict

Use a mesh when many services need the same behaviour, and you want it set in one place, not written many times. Keep retries small, since they multiply load. Accept the extra hop and the extra processes. Do not use one for a handful of services that a library can serve.

## How to recognise this in code you did not write

- Istio, Linkerd, Consul Connect or Cilium.
- Envoy proxies injected beside each pod.
- Policies written as YAML: retries, timeouts, allowed callers.
- Dashboards of calls between services with no code in the services.

## Where you have already met this

Kubernetes platforms at large companies, and Lyft, where Envoy began.

## When this is too much

For a few services, a shared library, or none, is simpler. A mesh is a system in itself, and needs people who understand it.
