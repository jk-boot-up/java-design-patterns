# Strangler Fig with NGINX Pattern — Video Narration Script

## 1. Strangler Fig with NGINX

Hello, and welcome. This video explains the Strangler Fig pattern in Java, using a real web server called NGINX. This video is presented by Jayasekhar Konduru. First, a simple definition. You replace an old system without switching it off. You grow the new one beside it, one piece at a time. Behind a single front door that decides, piece by piece, which system answers. In our online store, the old shop does everything: prices, stock, the basket, checkout, and past orders. A new service is being written to replace it. The front door sends prices to the new service, and everything else to the old shop. By the end, you will hear a route move with nothing restarting. An old rule quietly cancel that move. One slash change what the new service is asked for. And a cookie that only the old shop understands.

## 2. The Scenario

Here is the scenario. The old shop is one program that does everything. It shows prices and stock, keeps each basket, takes the checkout, and lists past orders. A team is writing its replacement, the new service. So far, it has built prices and checkout. The shop cannot stop trading while this happens. The plain Java version used a router written as a Java object, with one switch per part. This time, the router is a real one, running in a container, in front of two real web servers. And a real router has rules of its own.

## 3. The Big Bang

First demo: the big bang. Every web request gets a three-digit answer, called a status code. Two hundred means it worked. Four oh four means there is no such page. The front door starts with one rule: send everything to the old shop. The shop's four pages all answer two hundred: a price, a stock level, the basket, and an old order. Then the Monday of a big-bang switch. One line sends every route to the new service at once. The new service has built prices, so the price page works. The other three answer four oh four. One page in four works, on the busiest morning of the week.

## 4. NGINX's Words

NGINX brings a few words with it. Think of the reception desk in a big office building. Visitors never wander the corridors. They say who they want, and the receptionist sends them to the right floor, from a list. When a department moves, one line of the list changes, and visitors never notice. NGINX is the receptionist. A program that stands in front of others, and passes each request on, is called a reverse proxy. One line of its list is called a location. A location matches the start of a web address, called a prefix. The location that is just a slash matches everything, and that is where the old shop sits. And telling NGINX to re-read its list, without stopping, is called a reload.

## 5. One Route At A Time

Second demo: one route at a time. A customer's price request has already reached the old shop, and is still waiting for an answer. While it is open, the demo adds one location: prices go to the new service. Then it tells NGINX to reload. NGINX has one main process, which reads the list. And worker processes, which carry the requests. The main process is the same before and after the reload. Nothing restarted. For a moment, there are two workers. One is still finishing the open request. The other takes new ones. A new price request goes to the new service. Then the open request finishes, successfully, from the old shop. All four pages work: prices from the new service, and the other three from the old shop.

## 6. A Reload Has A Shape

A reload happens in steps, and it matters. First, the main process reads the new list. Second, it starts a new worker, using that list. Third, it tells the old worker: take nothing new, and finish what you have. Between the second and third steps, for a short moment, both workers take new requests. So a request in that moment could be answered using either list. An early version of this demo did not wait for that moment to pass. And in one run, the basket page was answered by the old shop, after the switch had already been made. So now, after every reload, the demo waits until only one worker is taking new requests.

## 7. Where Each Request Goes

Here is the whole setup, in words. The customer only ever knows one address: NGINX's. Every request goes there. Each route that has moved has its own location, sending it to the new service. Right now, that is prices. Everything else falls through to the catch-all, and goes to the old shop. Both services are real web servers, running inside the demo's Java program. And NGINX reaches them from its container, over the network. The rule to remember: move one route at a time, and the old shop serves the rest.

## 8. A Regular Expression Wins

Third demo, and the key finding of this project. The shop's real list has one more line, written years ago. It is written as a pattern of symbols, called a regular expression. And it says: any path starting with prices or stock goes to the old shop. The same move as before is added to that list. The settings check passes, and the reload succeeds. Ten price requests. All ten are answered by the old shop. None by the new service. The move did nothing, and nothing said so. Then the same line again, with two extra symbols in front: a caret and a tilde. Ten price requests, and all ten go to the new service.

## 9. How NGINX Picks A Location

Why did that happen? Because NGINX picks a location by its own rules. First, it finds the longest matching prefix, and remembers it. Second, it tries every regular expression, in the order written. Third, the first one that matches wins, and the remembered prefix is thrown away. Only if no regular expression matches does the prefix win. A caret and a tilde in front of a prefix change that. They tell NGINX: stop looking once this prefix matches. And the settings checker cannot warn you. Because nothing is wrong with the file. It does exactly what it says. A router written as a Java map cannot have this bug. A router with matching rules has it waiting in every old list.

## 10. One Slash

Fourth demo: one slash. Inside a location, one line says where to send the request. Here, it names the new service. With nothing after the name, NGINX passes the full path on, as it came. The new service is asked for the whole prices address, and succeeds. With one slash after the name, NGINX first cuts the matched part off the front of the path. So the new service is asked for just the product code. And it answers four oh four. One character, and every price request fails. The new service records every path it receives, which is how the demo knows exactly what arrived.

## 11. The New Service Goes Down

Fifth demo: the new service goes down. The old shop is still fine. Ten price requests get the answer five oh two, called bad gateway. That is NGINX saying the service behind it did not answer. No shop wrote that answer. NGINX did. Ten stock requests, still on the old shop, all succeed. Only the route that moved is hurt. Rolling back means removing one location, and one reload. The next ten price requests are answered by the old shop. When the new service comes back, one more reload moves prices to it again.

## 12. The Bill

Sixth demo: the bill. A customer puts three items in their basket. The old shop keeps the basket in its own memory. And it asks the browser to keep a small note, called a cookie, so it can find the basket again. Now checkout moves to the new service. NGINX passes the cookie along faithfully. But the new service has no idea what it means. So it answers: your basket is empty. To a customer with three items in it. Moved back to the old shop, the same checkout places the order: three items, forty-two pounds forty-nine. So checkout cannot move until the basket does. The old shop still serves four of the five routes. And now there are three things to run, not one: NGINX, the old shop, and the new service.

## 13. What The Simulation Left Out

So what did the plain Java version get right? The whole shape. Everything starts on the old system. A route moves with one switch, and moves back the same way, without touching the others. And the big bang fails on everything the new code has not built. All of that holds on NGINX. What it left out was the router being a real program. A reload, with a moment when two workers take requests. A path that one slash rewrites. And two services that can fail separately. And the headline. In the plain version, a switch was a switch. In NGINX, an old rule can beat the new one, and a move can do nothing, while every check says it worked. The plain version also compared both sides' answers before moving. NGINX can send a copy of a request, but it throws the copy's answer away.

## 14. The Verdict

So, here is the verdict. Put the proxy in front of the old system on day one. With one catch-all rule, sending everything to the old system. Then move routes, one location at a time. And settle four things, because NGINX will not. One. Write every moved route with the caret and tilde, so no old pattern can take it back. Two. Decide whether the new service expects the full path, and write the slash to match. Three. Wait for a reload to finish before trusting it. Four. Before a route moves, find every cookie it depends on, and check the new service can read it.

## 15. What Is Real, And When Not

A quick, honest note about this demo. NGINX is version one point thirty-one point six, in a container that the demo starts and stops by itself. The old shop and the new service are real web servers, built into Java. Every reload is real. And every bad gateway was written by NGINX. You just need Docker switched on first. So, when is this too much? If the old system is small enough to rewrite in a few weeks, months of running two systems cost more than they save. And if the two systems cannot share a customer's session, the routes that need it cannot be split. No proxy solves that for you.

## 16. Thanks for Watching

That's Strangler Fig, with NGINX. If you remember one sentence, make it this one. Move one route at a time, and check which rule really wins, because the router has rules of its own. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Move stock as well as prices, in the list with the old rule. Guess which service answers each, and then run it. If you found this useful, a like really helps other people discover it. Kindly subscribe to the channel. It helps the channel grow and bring you more content. Thanks for watching!
