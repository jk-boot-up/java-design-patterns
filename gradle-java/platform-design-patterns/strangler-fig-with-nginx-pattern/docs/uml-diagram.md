# Strangler Fig with NGINX Pattern — UML Sequence Diagrams

Four sequences. The regular expression that wins comes first, because it is the headline find and the one thing a router written as a Java object could never show.

## 1. A Regular Expression Wins

The configuration carries an old rule for caching catalogue reads, `location ~ ^/api/(prices|stock)/`, and gains a new one, `location /api/prices/`, to the new service. NGINX finds the prefix, then tries the regular expression, which matches and wins. 10 price requests out of 10 still reach the old shop.

![A regular expression wins](images/uml-diagram.png)

## 2. One Slash

The same route, with the new service's address written two ways. With nothing after the name, the path passes untouched. With a slash, NGINX cuts the matched prefix off.

![One slash](images/uml-diagram-2.png)

## 3. The New Service Goes Down

Prices are on the new service, and it stops. NGINX answers 502 itself for prices; stock, on the old shop, is unaffected. Rolling back is one location removed and one reload.

![The new service goes down](images/uml-diagram-3.png)

## 4. A Cookie Only One Side Understands

The old shop keeps the basket and finds it by its own cookie. NGINX passes the cookie to whichever service answers. The new service receives it and cannot use it.

![A cookie only one side understands](images/uml-diagram-4.png)

