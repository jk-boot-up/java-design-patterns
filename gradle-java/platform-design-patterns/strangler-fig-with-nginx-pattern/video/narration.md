# Strangler Fig with NGINX Pattern — Video Narration Script

## 1. Strangler Fig with NGINX

Hello, and welcome. This video explains the Strangler Fig pattern in Java, using a real web server called NGINX. It is written and presented by Jayasekhar Konduru. Here is the plain definition, in general words. You replace an old system without switching it off. You grow the new one beside it, one piece at a time, behind a single front door that decides, piece by piece, which system answers. Now the same thing in our online store. The old shop does everything: prices, stock, the basket, checkout and past orders. A new service is being written to replace it. Customers only ever talk to the front door, and the front door sends prices to the new service, and everything else to the old shop, until, one route at a time, nothing is left on the old one. By the end you will have seen a route move without anything restarting, an old rule quietly cancel that move, one slash change what the new service is asked for, and a cookie that only the old shop understands.

## 2. The Scenario

Here is the scenario. The old shop is one program that does everything. It shows prices and stock, keeps each customer's basket, takes the checkout, and lists past orders. A team is writing its replacement, the new service, and so far it has built prices and checkout. The shop cannot stop trading while that happens. The hand-built twin of this project put a router in front of both, written as a Java object with one switch per capability. This time the router is a real one, running in a container, in front of two real web servers. And a real router has rules of its own.

## 3. The Big Bang

First, the way people are tempted to do it. Every web request gets a three-digit answer first, called a status code. Two hundred means it worked. Four oh four means there is no such page. The front door starts with one rule: send everything to the old shop. The shop's four pages, a price, a stock level, the basket and an old order, all answer two hundred. Then the Monday of a big-bang migration. One line sends every route to the new service at once. The new service has built prices, so the price page works. The other three answer four oh four. One page in four works, on the busiest morning of the week.

## 4. NGINX's Words

NGINX brings a few words with it, and each one is simpler than it sounds. Think of the reception desk in a large office building. Visitors never wander the corridors. They say who they want, and the receptionist sends them to the right floor, from a list. When a department moves, one line of the list changes, and visitors never notice. NGINX is the receptionist. A program that stands in front of others and passes each request on is called a reverse proxy. One line of its list is called a location. A location matches the start of a web address, which NGINX calls a prefix, such as slash api slash prices slash. The location that is just a slash matches everything, and that is where the old shop sits. And telling NGINX to read its list again, without stopping, is called a reload.

## 5. One Route At A Time

Second, the pattern, on a real proxy. A customer's price request has already reached the old shop, and the old shop is slow to answer it. While it is still open, the demo adds one location to the list, prices to the new service, and tells NGINX to reload. NGINX has one main process, which reads the list, and worker processes, which carry the requests. The main process is number one before the reload, and number one after. Nothing restarted. For a moment there are two workers. One is still finishing the open request. The other takes new ones. A new price request goes to the new service. Then the open request finishes, with a two hundred, from the old shop. All four pages work. Prices from the new service, the other three from the old shop.

## 6. A Reload Has A Shape

A reload has a shape, and it matters. First, the main process reads the new list. Second, it starts a new worker that uses it. Third, it tells the old worker to take nothing new, and to finish what it already has. Between the second step and the third, for a short moment, both workers take new connections. A request sent in that moment can be answered under either list. An early version of this demo did not wait for that moment to pass, and in one of its first runs the basket page was answered by the old shop after the big bang had already been applied. So now, after every reload, the demo waits until NGINX answers with the new list, and only one worker is taking new connections.

## 7. Where Each Request Goes

Here is the whole arrangement, in words. The customer only ever knows one address, NGINX's. Every request goes there. Each route that has moved has a location of its own, sent to the new service. Right now that is prices. Everything else falls through to the one catch-all location, and goes to the old shop. Both shop services are real web servers, running inside the demo's own Java program, and NGINX reaches them from its container over the network. The rule to remember is this: move one route at a time, and the old shop serves the rest.

## 8. A Regular Expression Wins

Third, the find this project is built around. The shop's real list has one more line, written years ago, to let browsers keep catalogue pages for a minute. It is written as a regular expression, which is a pattern made of symbols, and this one means: any path starting with prices or stock goes to the old shop. The same move as before goes into that list. The check passes, and the reload succeeds. Ten price requests. Ten are answered by the old shop, and none by the new service. The move did nothing, and nothing said so. Then the same line, with two characters in front of the prefix: a caret and a tilde. Ten price requests, and all ten go to the new service.

## 9. How NGINX Picks A Location

Why did that happen? Because NGINX picks a location by rules of its own. First, it finds the longest prefix that matches the path, and remembers it. Second, it tries every regular expression, in the order they are written. Third, the first one that matches wins, and the remembered prefix is thrown away. Only if no regular expression matches does the prefix win. A caret and a tilde in front of a prefix change that. They tell NGINX to stop looking once the prefix matches. And the configuration checker cannot warn you, because nothing is wrong with the file. It does exactly what it says. A router written as a Java map cannot have this bug. A router with matching rules has it waiting in every old list.

## 10. One Slash

Fourth, one slash. Inside a location, a line called proxy pass says where to send the request. Here it names the new service. Written with nothing after the name, NGINX passes the path on as it came. The new service is asked for slash api slash prices slash S K U one, and answers two hundred. Written with one slash after the name, NGINX first cuts the part of the path the location matched off the front. The new service is asked for slash S K U one, and answers four oh four. One character, and every price request fails. The new service writes down every path it receives, which is how the demo knows exactly what arrived.

## 11. The New Service Goes Down

Fifth, the new service goes down, while the old shop is fine. Ten price requests get five oh two, which is called Bad Gateway. It is NGINX saying that the service behind it did not answer. No shop wrote that answer. NGINX did. Ten stock requests, still on the old shop, all get two hundred. Only the route that moved is hurt. Rolling back is removing the one location, and one reload. The next ten price requests are answered by the old shop. When the new service comes back, one more reload moves prices to it again.

## 12. The Bill

Sixth, the bill. A customer puts three items in the basket. The old shop keeps the basket in its own memory, and asks the browser to keep a small note, called a cookie, so it can find the basket again. This one is named legacy session. Now checkout moves to the new service. NGINX passes the cookie along faithfully. The new service receives it, and has no idea what it means. It answers four twenty two: your basket is empty, to a customer with three items in it. Moved back to the old shop, the same checkout places order one thousand and two, three items, four thousand two hundred and forty-nine pence. So checkout cannot move until the basket does. The old shop still serves four of the five routes. And there are three things to run now, not one: an NGINX container, the old shop and the new service, and a file that decides who answers.

## 13. What The Simulation Left Out

So what did the hand-built twin get right? The whole shape. Everything starts on the old system. A route moves with one switch, and moves back with the same switch, without touching the others. And the big bang fails on everything the new code has not built. All of that holds on NGINX. What it left out was the router being a real program. A reload, with a moment when two workers take requests. A path that one slash rewrites. And two services that can go down separately. And the headline: in the twin, a switch was a switch. In NGINX, an old rule can win against the new one, and a move can do nothing at all while every check says it worked. The twin also had something NGINX does not: it compared the two sides' answers before moving. NGINX can send a copy of a request, but it throws the copy's answer away.

## 14. The Verdict

The verdict. Put the proxy in front of the old system on day one, with one catch-all rule to the old system, and move routes by adding one location each. Then say four things out loud, because NGINX will not. Write every moved route with the caret and tilde, so no old pattern can take it back. Decide whether the new service expects the full path, and write the slash to match. Wait for a reload to finish before trusting it. And before a route moves, find every cookie it depends on, and check the new service can read it.

## 15. What Is Real, And When Not

What in this project is real? NGINX version one point thirty-one point six, in a container the demo starts and stops itself, run by a library called Testcontainers. The old shop and the new service are real web servers, the one built into Java. Every reload is a real reload, and every five oh two was written by NGINX. And when is this too much? If the old system is small enough to rewrite in a few weeks, the months of running two systems cost more than they save. And if the two systems cannot share a customer's session, the routes that need it cannot be split, and no proxy solves that for you.

## 16. Thanks for Watching

That's Strangler Fig with NGINX. If you take one sentence away, take this one: move one route at a time, and check which rule really wins, because the router has rules of its own. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository. If you try one exercise, move stock as well as prices, in the list with the old rule, guess which service answers each, and then run it. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
