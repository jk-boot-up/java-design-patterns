"""Scene definitions for the Strangler Fig with NGINX teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks every count out loud, says each of NGINX's words in plain
language before using NGINX's name for it, and never points at a picture the
listener cannot see. Every figure is the output of `./gradlew run`.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Strangler Fig with NGINX',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Strangler Fig pattern in Java, using a real web server '
            'called NGINX. [[slnc 300]] This video is presented by '
            'Jayasekhar Konduru. [[slnc 600]] First, a simple definition. '
            '[[slnc 300]] You replace an old system without switching it '
            'off. [[slnc 300]] You grow the new one beside it, one piece '
            'at a time. [[slnc 300]] Behind a single front door that '
            'decides, piece by piece, which system answers. [[slnc 700]] '
            'In our online store, the old shop does everything: prices, '
            'stock, the basket, checkout, and past orders. [[slnc 300]] A '
            'new service is being written to replace it. [[slnc 300]] The '
            'front door sends prices to the new service, and everything '
            'else to the old shop. [[slnc 500]] By the end, you will hear '
            'a route move with nothing restarting. [[slnc 300]] An old '
            'rule quietly cancel that move. [[slnc 300]] One slash change '
            'what the new service is asked for. [[slnc 300]] And a cookie '
            'that only the old shop understands.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['The old shop does everything:', 'prices, stock, basket, checkout, orders.', '',
              'The new service has built', 'prices and checkout, so far.', '',
              'The shop cannot stop trading.', 'Nobody wants a cutover weekend.', '',
              'This time the front door is', 'a real NGINX, in a container.'],
        narration=(
            'Here is the scenario. [[slnc 400]] The old shop is one '
            'program that does everything. [[slnc 300]] It shows prices '
            'and stock, keeps each basket, takes the checkout, and lists '
            'past orders. [[slnc 500]] A team is writing its replacement, '
            'the new service. [[slnc 300]] So far, it has built prices '
            'and checkout. [[slnc 500]] The shop cannot stop trading '
            'while this happens. [[slnc 600]] The plain Java version used '
            'a router written as a Java object, with one switch per part. '
            '[[slnc 300]] This time, the router is a real one, running in '
            'a container, in front of two real web servers. [[slnc 300]] '
            'And a real router has rules of its own.'
        ),
    ),
    dict(
        key='03-one', kind='console', title='The Big Bang',
        body="""ONE. The big bang.
  every route to the old shop:
  prices 200, stock 200,
  basket 200, orders 200.
  pages that work: 4 of 4

  Monday: every route to the new service.
  prices 200, stock 404,
  basket 404, orders 404.
  pages that work: 1 of 4""",
        narration=(
            'First demo: the big bang. [[slnc 400]] Every web request '
            'gets a three-digit answer, called a status code. [[slnc '
            '300]] Two hundred means it worked. [[slnc 300]] Four oh four '
            'means there is no such page. [[slnc 600]] The front door '
            'starts with one rule: send everything to the old shop. '
            "[[slnc 300]] The shop's four pages all answer two hundred: a "
            'price, a stock level, the basket, and an old order. [[slnc '
            '600]] Then the Monday of a big-bang switch. [[slnc 300]] One '
            'line sends every route to the new service at once. [[slnc '
            '300]] The new service has built prices, so the price page '
            'works. [[slnc 300]] The other three answer four oh four. '
            '[[slnc 300]] One page in four works, on the busiest morning '
            'of the week.'
        ),
    ),
    dict(
        key='04-words', kind='bullets', title="NGINX's Words",
        body=['A reverse proxy stands in front,', 'and passes each request on.', '',
              'A location is one line of its list.', 'It matches the start of a path:', 'a prefix, like /api/prices/', '',
              'location /  matches everything.', '', 'A reload: read the list again.'],
        narration=(
            'NGINX brings a few words with it. [[slnc 400]] Think of the '
            'reception desk in a big office building. [[slnc 300]] '
            'Visitors never wander the corridors. [[slnc 300]] They say '
            'who they want, and the receptionist sends them to the right '
            'floor, from a list. [[slnc 300]] When a department moves, '
            'one line of the list changes, and visitors never notice. '
            '[[slnc 600]] NGINX is the receptionist. [[slnc 300]] A '
            'program that stands in front of others, and passes each '
            'request on, is called a reverse proxy. [[slnc 500]] One line '
            'of its list is called a location. [[slnc 300]] A location '
            'matches the start of a web address, called a prefix. [[slnc '
            '300]] The location that is just a slash matches everything, '
            'and that is where the old shop sits. [[slnc 500]] And '
            'telling NGINX to re-read its list, without stopping, is '
            'called a reload.'
        ),
    ),
    dict(
        key='05-two', kind='console', title='One Route At A Time',
        body="""TWO. One route at a time.
  a price request is open on the old shop.
  location /api/prices/ added. reload.
  main process: number 1 before, number 1 after.

  still finishing old requests: 1.
  taking new requests: 1.
  a new price request: 200, new service.
  the open request: 200, from the old shop.
  pages that work: 4 of 4
  (3 from the old shop, 1 from the new service)""",
        narration=(
            "Second demo: one route at a time. [[slnc 400]] A customer's "
            'price request has already reached the old shop, and is still '
            'waiting for an answer. [[slnc 500]] While it is open, the '
            'demo adds one location: prices go to the new service. [[slnc '
            '300]] Then it tells NGINX to reload. [[slnc 600]] NGINX has '
            'one main process, which reads the list. [[slnc 300]] And '
            'worker processes, which carry the requests. [[slnc 300]] The '
            'main process is the same before and after the reload. [[slnc '
            '300]] Nothing restarted. [[slnc 600]] For a moment, there '
            'are two workers. [[slnc 300]] One is still finishing the '
            'open request. [[slnc 300]] The other takes new ones. [[slnc '
            '500]] A new price request goes to the new service. [[slnc '
            '300]] Then the open request finishes, successfully, from the '
            'old shop. [[slnc 500]] All four pages work: prices from the '
            'new service, and the other three from the old shop.'
        ),
    ),
    dict(
        key='06-reload', kind='bullets', title='A Reload Has A Shape',
        body=['1. The main process reads the new list.', '2. It starts a new worker with it.',
              '3. It tells the old worker: take nothing', '   new, and finish what you have.', '',
              'Between 2 and 3, both workers take', 'new connections, for a moment.', '',
              'So the demo waits until only one', 'worker takes new connections.'],
        narration=(
            'A reload happens in steps, and it matters. [[slnc 500]] '
            'First, the main process reads the new list. [[slnc 300]] '
            'Second, it starts a new worker, using that list. [[slnc '
            '300]] Third, it tells the old worker: take nothing new, and '
            'finish what you have. [[slnc 600]] Between the second and '
            'third steps, for a short moment, both workers take new '
            'requests. [[slnc 300]] So a request in that moment could be '
            'answered using either list. [[slnc 600]] An early version of '
            'this demo did not wait for that moment to pass. [[slnc 300]] '
            'And in one run, the basket page was answered by the old '
            'shop, after the switch had already been made. [[slnc 500]] '
            'So now, after every reload, the demo waits until only one '
            'worker is taking new requests.'
        ),
    ),
    dict(
        key='07-diagram', kind='diagram', title='Where Each Request Goes',
        body=None,
        narration=(
            'Here is the whole setup, in words. [[slnc 400]] The customer '
            "only ever knows one address: NGINX's. [[slnc 300]] Every "
            'request goes there. [[slnc 500]] Each route that has moved '
            'has its own location, sending it to the new service. [[slnc '
            '300]] Right now, that is prices. [[slnc 300]] Everything '
            'else falls through to the catch-all, and goes to the old '
            'shop. [[slnc 500]] Both services are real web servers, '
            "running inside the demo's Java program. [[slnc 300]] And "
            'NGINX reaches them from its container, over the network. '
            '[[slnc 500]] The rule to remember: move one route at a time, '
            'and the old shop serves the rest.'
        ),
    ),
    dict(
        key='08-three', kind='console', title='A Regular Expression Wins',
        body="""THREE. A regular expression wins.
  an old rule, written years ago:
  location ~ ^/api/(prices|stock)/

  the same move: location /api/prices/
  10 price requests:
  10 from the old shop, 0 from the new service

  location ^~ /api/prices/
  10 price requests:
  0 from the old shop, 10 from the new service""",
        narration=(
            'Third demo, and the key finding of this project. [[slnc '
            "400]] The shop's real list has one more line, written years "
            'ago. [[slnc 300]] It is written as a pattern of symbols, '
            'called a regular expression. [[slnc 300]] And it says: any '
            'path starting with prices or stock goes to the old shop. '
            '[[slnc 600]] The same move as before is added to that list. '
            '[[slnc 300]] The settings check passes, and the reload '
            'succeeds. [[slnc 500]] Ten price requests. [[slnc 300]] All '
            'ten are answered by the old shop. [[slnc 300]] None by the '
            'new service. [[slnc 300]] The move did nothing, and nothing '
            'said so. [[slnc 600]] Then the same line again, with two '
            'extra symbols in front: a caret and a tilde. [[slnc 300]] '
            'Ten price requests, and all ten go to the new service.'
        ),
    ),
    dict(
        key='09-rules', kind='bullets', title='How NGINX Picks A Location',
        body=['1. Find the longest matching prefix.', '   Remember it.',
              '2. Try each regular expression,', '   in the order written.',
              '3. The first one that matches wins.', '4. None matched? The prefix wins.', '',
              '^~ in front of a prefix:', 'stop looking once it matches.', '',
              'nginx -t cannot see this. It is valid.'],
        narration=(
            'Why did that happen? [[slnc 300]] Because NGINX picks a '
            'location by its own rules. [[slnc 600]] First, it finds the '
            'longest matching prefix, and remembers it. [[slnc 300]] '
            'Second, it tries every regular expression, in the order '
            'written. [[slnc 300]] Third, the first one that matches '
            'wins, and the remembered prefix is thrown away. [[slnc 300]] '
            'Only if no regular expression matches does the prefix win. '
            '[[slnc 600]] A caret and a tilde in front of a prefix change '
            'that. [[slnc 300]] They tell NGINX: stop looking once this '
            'prefix matches. [[slnc 600]] And the settings checker cannot '
            'warn you. [[slnc 300]] Because nothing is wrong with the '
            'file. [[slnc 300]] It does exactly what it says. [[slnc '
            '500]] A router written as a Java map cannot have this bug. '
            '[[slnc 300]] A router with matching rules has it waiting in '
            'every old list.'
        ),
    ),
    dict(
        key='10-four', kind='code', title='One Slash',
        body="""// passes the path on as it came
proxy_pass http://new_service;
//   asked for /api/prices/SKU-1   ->  200

// cuts the matched prefix off first
proxy_pass http://new_service/;
//   asked for /SKU-1              ->  404""",
        narration=(
            'Fourth demo: one slash. [[slnc 400]] Inside a location, one '
            'line says where to send the request. [[slnc 300]] Here, it '
            'names the new service. [[slnc 600]] With nothing after the '
            'name, NGINX passes the full path on, as it came. [[slnc '
            '300]] The new service is asked for the whole prices address, '
            'and succeeds. [[slnc 600]] With one slash after the name, '
            'NGINX first cuts the matched part off the front of the path. '
            '[[slnc 300]] So the new service is asked for just the '
            'product code. [[slnc 300]] And it answers four oh four. '
            '[[slnc 500]] One character, and every price request fails. '
            '[[slnc 300]] The new service records every path it receives, '
            'which is how the demo knows exactly what arrived.'
        ),
    ),
    dict(
        key='11-five', kind='console', title='The New Service Goes Down',
        body="""FIVE. The new service goes down.
  10 price requests:
  10 answered 502 Bad Gateway, by NGINX itself.
  10 stock requests:
  10 answered 200, by the old shop.

  roll back: one location removed, a reload.
  10 price requests:
  10 answered 200, by the old shop.""",
        narration=(
            'Fifth demo: the new service goes down. [[slnc 400]] The old '
            'shop is still fine. [[slnc 500]] Ten price requests get the '
            'answer five oh two, called bad gateway. [[slnc 300]] That is '
            'NGINX saying the service behind it did not answer. [[slnc '
            '300]] No shop wrote that answer. [[slnc 300]] NGINX did. '
            '[[slnc 500]] Ten stock requests, still on the old shop, all '
            'succeed. [[slnc 300]] Only the route that moved is hurt. '
            '[[slnc 600]] Rolling back means removing one location, and '
            'one reload. [[slnc 300]] The next ten price requests are '
            'answered by the old shop. [[slnc 300]] When the new service '
            'comes back, one more reload moves prices to it again.'
        ),
    ),
    dict(
        key='12-bill', kind='console', title='The Bill',
        body="""SIX. The bill.
  3 items in the basket, on the old shop.
  cookie: LEGACYSESSION=L-1

  checkout on the new service:
  422, your basket is empty.
  checkout on the old shop: 200,
  order 1002 placed: 3 items, 4249 pence.

  the old shop still serves 4 of 5 routes.
  three things to run now, not one.""",
        narration=(
            'Sixth demo: the bill. [[slnc 400]] A customer puts three '
            'items in their basket. [[slnc 300]] The old shop keeps the '
            'basket in its own memory. [[slnc 300]] And it asks the '
            'browser to keep a small note, called a cookie, so it can '
            'find the basket again. [[slnc 600]] Now checkout moves to '
            'the new service. [[slnc 300]] NGINX passes the cookie along '
            'faithfully. [[slnc 300]] But the new service has no idea '
            'what it means. [[slnc 300]] So it answers: your basket is '
            'empty. [[slnc 300]] To a customer with three items in it. '
            '[[slnc 600]] Moved back to the old shop, the same checkout '
            'places the order: three items, forty-two pounds forty-nine. '
            '[[slnc 600]] So checkout cannot move until the basket does. '
            '[[slnc 300]] The old shop still serves four of the five '
            'routes. [[slnc 300]] And now there are three things to run, '
            'not one: NGINX, the old shop, and the new service.'
        ),
    ),
    dict(
        key='13-contrast', kind='bullets', title='What The Simulation Left Out',
        body=['Got right: the whole shape.', 'One switch per route, rollback per route,', 'the big bang failing.', '',
              'Left out: a reload, and its moment.', 'Left out: a path rewritten by a slash.',
              'Left out: one side down alone.', '',
              'Headline: an old regular expression', 'beats the move. 10 of 10 to the old shop.'],
        narration=(
            'So what did the plain Java version get right? [[slnc 400]] '
            'The whole shape. [[slnc 300]] Everything starts on the old '
            'system. [[slnc 300]] A route moves with one switch, and '
            'moves back the same way, without touching the others. [[slnc '
            '300]] And the big bang fails on everything the new code has '
            'not built. [[slnc 300]] All of that holds on NGINX. [[slnc '
            '600]] What it left out was the router being a real program. '
            '[[slnc 300]] A reload, with a moment when two workers take '
            'requests. [[slnc 300]] A path that one slash rewrites. '
            '[[slnc 300]] And two services that can fail separately. '
            '[[slnc 600]] And the headline. [[slnc 300]] In the plain '
            'version, a switch was a switch. [[slnc 300]] In NGINX, an '
            'old rule can beat the new one, and a move can do nothing, '
            'while every check says it worked. [[slnc 600]] The plain '
            "version also compared both sides' answers before moving. "
            '[[slnc 300]] NGINX can send a copy of a request, but it '
            "throws the copy's answer away."
        ),
    ),
    dict(
        key='14-verdict', kind='bullets', title='The Verdict',
        body=['Put the proxy in front on day one,', 'with one catch-all to the old shop.', '',
              'Move each route with ^~.', 'Write the slash on purpose.', '',
              'Wait for a reload to finish.', '',
              'Find every cookie a route needs', 'before the route moves.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Put the proxy in front '
            'of the old system on day one. [[slnc 300]] With one '
            'catch-all rule, sending everything to the old system. [[slnc '
            '300]] Then move routes, one location at a time. [[slnc 600]] '
            'And settle four things, because NGINX will not. [[slnc 500]] '
            'One. [[slnc 200]] Write every moved route with the caret and '
            'tilde, so no old pattern can take it back. [[slnc 400]] Two. '
            '[[slnc 200]] Decide whether the new service expects the full '
            'path, and write the slash to match. [[slnc 400]] Three. '
            '[[slnc 200]] Wait for a reload to finish before trusting it. '
            '[[slnc 400]] Four. [[slnc 200]] Before a route moves, find '
            'every cookie it depends on, and check the new service can '
            'read it.'
        ),
    ),
    dict(
        key='15-real', kind='bullets', title='What Is Real, And When Not',
        body=['Real: NGINX 1.31.6 in a container', 'the demo starts and stops.', 'Testcontainers 2.0.5.', '',
              'Real: two HTTP servers, a real reload,', 'a real 502.', '',
              'Too much: a system small enough', 'to rewrite in a few weeks.', '',
              'Not solved by a proxy: a shared session.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 400]] NGINX is '
            'version one point thirty-one point six, in a container that '
            'the demo starts and stops by itself. [[slnc 300]] The old '
            'shop and the new service are real web servers, built into '
            'Java. [[slnc 300]] Every reload is real. [[slnc 300]] And '
            'every bad gateway was written by NGINX. [[slnc 300]] You '
            'just need Docker switched on first. [[slnc 600]] So, when is '
            'this too much? [[slnc 300]] If the old system is small '
            'enough to rewrite in a few weeks, months of running two '
            'systems cost more than they save. [[slnc 300]] And if the '
            "two systems cannot share a customer's session, the routes "
            'that need it cannot be split. [[slnc 300]] No proxy solves '
            'that for you.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough',
              'are in the repository. Try the exercises in',
              'the session guide.'],
        narration=(
            "That's Strangler Fig, with NGINX. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] Move '
            'one route at a time, and check which rule really wins, '
            'because the router has rules of its own. [[slnc 500]] The '
            'full source code, written notes, diagrams, and an animated '
            'walkthrough are all in the repository. [[slnc 500]] Here is '
            'one exercise to try. [[slnc 300]] Move stock as well as '
            'prices, in the list with the old rule. [[slnc 300]] Guess '
            'which service answers each, and then run it. [[slnc 500]] If '
            'this helped, a like really does help other people find it. '
            "[[slnc 300]] And subscribe, if you'd like the rest of the "
            'series. [[slnc 400]] Thanks for watching.'
        ),
    ),
]
