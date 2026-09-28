# Strangler Fig with NGINX, Explained

## The pattern in one sentence

A strangler fig replaces an old system by growing the new one around it, one piece at a time, behind a single front door that decides, piece by piece, which system answers.

## The analogy, before any of NGINX's words

Think of the reception desk in a large office building. Visitors never wander the corridors. They tell the receptionist who they want, and the receptionist sends them to the right floor from a list. The company is moving, department by department, into a new building next door. When the accounts team moves, the receptionist's list changes one line, and visitors asking for accounts are sent next door. Everybody else still goes upstairs. No visitor ever notices a move.

Now four things the receptionist makes you think about. The receptionist reads the list by rules of their own, and an old sticky note on the desk that says "anyone asking about money, upstairs" can quietly beat the new line on the list. The way the receptionist writes a room number on a visitor's slip can change which room the visitor asks for when they arrive. When the list changes mid-morning, a visitor already on their way upstairs should still be seen, not turned back. And if the new building's door is locked, only the visitors sent there are stuck; everybody else is fine. Those four things, and one bill, are this project.

## What NGINX calls these things

**NGINX** is the receptionist: a web server used here as a **reverse proxy**, a program that stands in front of other programs, takes every request, and passes it to whichever one should answer. It runs in a container the demo starts and stops.

The **old shop** does everything: prices, stock, the basket, checkout and orders. The **new service** is the rewrite, and so far it has built prices and checkout. Both are real web servers running inside the demo's own Java program. NGINX reaches them from its container by the name `host.testcontainers.internal`.

A **location** block is one line of the receptionist's list. It matches the start of a web address, called a **prefix**, such as `/api/prices/`. The catch-all prefix `/` matches everything.

A **regular expression** is a pattern for matching text, written with symbols. `^/api/(prices|stock)/` means "starts with /api/prices/ or /api/stock/". A location marked with `~` uses one.

NGINX picks a location like this. It finds the longest matching prefix and remembers it. Then it tries the regular-expression locations, in the order they are written, and the first one that matches wins. Only if none matches does the remembered prefix win. A prefix written with **`^~`** in front tells NGINX to stop looking once it matches, and skip the regular expressions.

**`proxy_pass`** says where to send the request. **`upstream`** gives a name to a service's address, here `old_shop` and `new_service`. Written with nothing after the name, `proxy_pass` passes the path on untouched; written with anything after it, even one slash, it cuts the matched prefix off first.

**`nginx -t`** checks a configuration without using it, and **`nginx -s reload`** tells NGINX to start using it. NGINX's **main process** reads the configuration and never restarts; its **worker processes** handle the requests, and a reload replaces them.

An **HTTP status code** is the three-digit answer every web request gets first. 200 is success, 404 is no such page, 422 is "understood, and refused", and **502 Bad Gateway** is NGINX saying the service behind it did not answer.

A **cookie** is a small note a site asks the browser to keep and send back with every request. The old shop's is called `LEGACYSESSION`, and it is how the old shop finds a customer's basket.

## The six acts

### The Big Bang

NGINX starts in front of the old shop, with one rule: everything to the old shop. The shop's four pages — a price, a stock level, the basket and an old order — all answer 200, all from the old shop. Then the Monday of a big-bang migration: one line sends every route to the new service. The new service has built only prices and checkout, so the price page works and the other three answer 404. One page in four works.

```
  NGINX 1.31.6 is running in a container, in front of the old shop. every route goes to the old shop.
  the shop's four pages: prices 200, stock 200, basket 200, orders 200. pages that work: 4 of 4 (4 from the old shop, 0 from the new service).
  Monday: one line sends every route to the new service, which has built only prices and checkout so far.
  the four pages: prices 200, stock 404, basket 404, orders 404. pages that work: 1 of 4 (0 from the old shop, 1 from the new service).
```

### One Route At A Time

The pattern, on a real proxy. A customer's price request has already reached the old shop, and the old shop is slow to answer it. While it is open, the configuration gains one location, `/api/prices/`, sent to the new service, and NGINX reloads. Its main process is number 1 before and after: nothing restarted. While the old request is still open there are two workers: 1 still finishing old requests, and 1 taking new ones. A new price request goes to the new service. Then the open request finishes, with a 200, from the old shop, and the old worker exits. The four pages all work: prices from the new service, the other three from the old shop.

One detail the demo has to respect. A reload is not instant. NGINX starts the new worker first, then tells the old worker to stop taking new connections. For a short moment both take new connections, and a request sent then can be answered under either configuration. So the demo, after every reload, waits until NGINX answers with the new configuration's number and exactly one worker is taking new connections. An early version of this demo waited only for the first condition, and in one of its first runs the basket page was answered by the old shop after the big bang had already been applied.

```
  a customer's price request has reached the old shop, and the old shop is slow to answer it.
  the configuration gains location /api/prices/, sent to the new service. nginx -s reload.
  NGINX's main process: number 1 before the reload and number 1 after. nothing restarted.
  while that request is still open: workers still finishing old requests: 1. workers taking new requests: 1.
  a new price request: 200, from the new service.
  the open request then finishes: 200, from the old shop. workers still finishing old requests: 0.
  the four pages now: prices 200, stock 200, basket 200, orders 200. pages that work: 4 of 4 (3 from the old shop, 1 from the new service).
```

### A Regular Expression Wins

The headline find. The shop's real configuration has one more rule, written years ago to let browsers cache catalogue reads for a minute: `location ~ ^/api/(prices|stock)/`, sent to the old shop. The same move as before — `location /api/prices/`, to the new service — goes into that configuration. `nginx -t` finds nothing wrong, and the reload succeeds. Ten price requests: ten from the old shop, none from the new service. NGINX found the prefix, then tried the regular expression, which matched, and won. The move did nothing, and nothing said so. Written as `location ^~ /api/prices/`, which tells NGINX to stop looking once the prefix matches, all ten go to the new service.

```
  the shop's real configuration has one more rule, written years ago to cache catalogue reads: location ~ ^/api/(prices|stock)/
  the same move, location /api/prices/, in that configuration, and a reload. 10 price requests: 10 from the old shop, 0 from the new service.
  NGINX tries its regular-expression rules after finding the longest prefix, and the first one that matches wins. the move did nothing, and nothing said so.
  written as location ^~ /api/prices/, which tells NGINX to stop looking: 10 price requests: 0 from the old shop, 10 from the new service.
```

### One Slash

The new service's address is written two ways that differ by one character. Without a slash after the name, NGINX passes the path on as it came: the new service is asked for `/api/prices/SKU-1`, and answers 200. With a slash, NGINX cuts the matched prefix, `/api/prices/`, off the path and puts the slash in its place: the new service is asked for `/SKU-1`, and answers 404. The new service writes down every path it receives, which is how the demo knows exactly what arrived.

```
  proxy_pass http://new_service; the new service is asked for /api/prices/SKU-1 and answers 200.
  proxy_pass http://new_service/; the new service is asked for /SKU-1 and answers 404.
  with anything after the address, even one slash, NGINX cuts the matched prefix off the path it passes on.
```

### The New Service Goes Down

Prices are on the new service, and the new service stops. Ten price requests: ten answers of 502 Bad Gateway, written by NGINX itself, because nobody answered behind it. Ten stock requests, still on the old shop: ten answers of 200. Only the moved route is hurt. Rolling back is removing the one location block and reloading; the next ten price requests are answered by the old shop. When the new service is back, one more reload moves prices to it again.

```
  10 price requests: 10 answered 502 Bad Gateway, by NGINX itself. 10 stock requests: 10 answered 200, by the old shop.
  roll back: the one location removed, and a reload. 10 price requests: 10 answered 200, by the old shop.
  the new service comes back, and one more reload moves prices to it again: 10 price requests: 0 from the old shop, 10 from the new service.
```

### The Bill

A customer puts three items in the basket. The old shop keeps the basket in its own memory and sets a cookie, `LEGACYSESSION=L-1`, so it can find the basket again. Checkout moves to the new service. NGINX passes the cookie along faithfully, and the new service receives `LEGACYSESSION=L-1` — and has no idea what it means, because it keeps its own baskets under its own cookie. It answers 422: your basket is empty, to a customer with three items in it. Moved back to the old shop, the same checkout places order 1002: three items, 4249 pence. Checkout cannot move until the basket does, or until both services agree on one session. The old shop still serves four of the five routes. And there are now three things to run, not one: an NGINX container, the old shop and the new service, and a configuration file that decides who answers.

```
  a customer puts 3 items in the basket. the old shop answers "basket: 3 items" and sets the cookie LEGACYSESSION=L-1.
  checkout moves to the new service. it receives the cookie LEGACYSESSION=L-1 and has no use for it: 422, your basket is empty.
  checkout moved back to the old shop: 200, order 1002 placed: 3 items, 4249 pence.
  checkout cannot move until the basket does. the old shop still serves 4 of 5 routes: stock, basket, checkout and orders.
  and three things to run now, not one: 1 NGINX container, the old shop and the new service, and a configuration file that decides who answers.
```

## What this project does not show

- **Shadow reads.** The plain-Java twin sent orders to both sides and compared the answers before moving anything. NGINX's `mirror` directive can send a copy of a request to the new service, but it throws the copy's answer away; comparing the two needs a program of its own.
- **A migration that stalls.** The twin modelled the cost of a migration that stops half-finished. That is about budgets and people, and no proxy shows it.
- **Two teams and two release calendars.** Here both services run in one Java program on one machine. The network between NGINX and them is real; the organisation around them is not.

## The verdict

Put a real proxy in front of the old system on day one, with one catch-all rule to the old system, and move routes by adding one location each. Then say three things out loud, because NGINX will not: write every moved route with `^~`, or check that no regular-expression location can take it back; decide deliberately whether the new service expects the full path or not, and write the slash to match; and wait for a reload to finish before trusting the new configuration. Before moving a route, find every cookie and header it depends on, and whether the new service can read them.

## How to recognise this in code you did not write

- A gateway configuration with one catch-all `location /` to an old system and a growing list of specific locations to new ones. That is a strangler fig.
- A `location ~` or `location ~*` anywhere above the moved routes. Check whether it matches any of them; if it does, it wins.
- A `proxy_pass` with a path, or just a slash, after the address. That location rewrites every path it passes on.
- A restart, rather than `nginx -t` and `nginx -s reload`, in the deploy script. That drops the requests in progress.
- A session cookie set by the old system and read by routes that are about to move.

## Where you have already met this

Any migration with an `/api/v2` running beside an `/api/v1`, behind NGINX, HAProxy, Envoy, a cloud load balancer or an API gateway. Each has its own order of matching rules, its own way of rewriting paths, and its own way of changing rules without dropping requests.

## When this is too much

If the old system can be rewritten and replaced in a few weeks, the router and the months of running two systems cost more than they save. And if the old and new systems cannot share a session, the routes that depend on it cannot be split until that is solved.
