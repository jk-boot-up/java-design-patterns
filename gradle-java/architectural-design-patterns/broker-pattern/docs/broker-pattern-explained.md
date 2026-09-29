# Broker, Explained

## The pattern in one sentence

A broker sits between clients and services, lets services register by name
and forwards clients' calls by name, so neither side needs the other's
address.

## The 5 acts

### 1. A hard-coded address

Checkout knows the stock service's address and asks it directly: 4 kettles
in stock. The stock service is moved to a new machine, with a new address.
Checkout still uses the old one, and every call fails: connection refused.

### 2. Calls through a broker

The stock service registers with the broker under the name "stock". Checkout
sends `/call/stock?sku=KETTLE-1` to the broker, which looks up the name,
forwards the call and returns 4. Checkout knows only the broker's address.

### 3. A service moves

The stock service moves again and registers its new address with the broker.
Checkout does not change at all, and its next call, for mugs, returns 20.

### 4. Several instances

Two instances of the price service register under the same name. Four calls
from checkout are answered by price-a, price-b, price-a, price-b: the broker
takes turns, and checkout never chose an instance.

### 5. The bill

Every call from checkout is now two network requests, checkout to broker and
broker to service. And when the broker stops, every service is unreachable,
even though they are all still running; real brokers run as several copies.

## The verdict

Use a broker, or a registry doing the same job, when services move, scale or
change often. Run it redundantly, keep it fast, and consider client-side
lookup to avoid the extra hop.

## How to recognise this in code you did not write

- Calls addressed by service name rather than host and port.
- A registry that services announce themselves to at start-up.
- Round-robin between instances with the same name.

## Where you have already met this

- Java RMI's registry and CORBA's object request broker.
- Service registries such as Consul, Eureka and etcd.
- Kubernetes services, which give a stable name to moving pods.
- API gateways and service meshes that route calls by name.
