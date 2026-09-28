# API Gateway Pattern — Video Narration Script

## 1. API Gateway

Hello, and welcome. This video explains the A P I Gateway pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. An A P I gateway is one service placed in front of all the others. So a client makes a single call, instead of five, and only needs to know one address. The gateway asks whichever services it needs, joins their answers, and sends back one reply. Think of a hotel reception desk. You do not phone housekeeping, the restaurant, and the concierge separately. You ring reception, and reception deals with the rest. In our online store, the product page is built from four different services. By the end, you will know why one call beats four, even when four calls work perfectly. What a gateway must never start doing. And how deciding in advance which services matter keeps the shop selling when one of them stops answering.

## 2. The Scenario

Here is the scenario. The shop's mobile app has a product page for an espresso machine. To draw it, the app needs four pieces of information, owned by four services. The name and description come from the catalog service. The price comes from the pricing service. Whether it is in stock comes from the inventory service. And the row of suggestions, customers also bought, comes from a recommendations service. The obvious design is an app that makes four calls, and puts the answers together. To be fair, it works. It shows the right page, and every test passes. Its problems only show up on the clock, and on the day something goes wrong.

## 3. Four Calls From a Phone on a Train

Let's put numbers on it. A round trip from a phone on a train to a data centre takes about two hundred milliseconds. Most of that is distance and radio, not work. Four calls, one after another, is eight hundred milliseconds. Eight hundred milliseconds of a shopper staring at a half-drawn screen. Second, each service must check that the caller is a signed-in shopper. So the access token is checked four times, for one page, in four different codebases. Third, the app knows four addresses. So when a service is moved or split, the app on the phone must change. And you cannot simply update a phone. You release a new version, and wait months for people to install it.

## 4. The Naive Approach — The App Does the Joining

The naive app's product page method is four ordinary lines of Java. Ask catalog for the product. Ask pricing for the price. Ask inventory for the stock. Ask recommendations for the suggestions. Then build one page from the four answers. Nothing is badly written. What is wrong is what is missing. There is no line saying which answers the page truly needs, and which it could live without. All four are called the same way, so all four are treated as equally important. So the page fails whenever any one of them fails. The suggestions row has become essential, and nobody decided that.

## 5. Why That Hurts

So what exactly is wrong? Five separate costs. One. The waiting adds up, on the slowest link in the system: the phone's connection. Two. The token is checked four times, in four codebases, for one page. Three. The app is tied to the layout of the back end. Every reorganisation means changing the phone app, the slowest thing in the company to change. Four. Every kind of client repeats the same work. The website, the app, and the in-store till each join the same four answers. And five, the expensive one. When the recommendations service stops answering, the whole product page is lost. The name, price, and stock had all arrived. And all are thrown away, because a feature nobody would miss did not answer.

## 6. The API Gateway Pattern

Here is the pattern, as it is usually stated. A service that is the entry point into the system from the outside world. It sends each request to the right service, or joins the results of several. In plain words: one front door. The client asks once, at one address. Behind that door, the gateway does all the asking around. And returns one answer, already shaped the way the client wants to show it. That gives you one trip across the slow network, instead of four. One place to check the token. One address for the client to know. And one place where someone decides what happens when a service does not answer.

## 7. An Analogy

Here is the analogy to hold on to: a hotel reception desk. You want fresh towels, and a table in the restaurant at eight. You do not phone housekeeping and the restaurant separately. You ring reception, and reception handles it. One number to remember. It does not change when the hotel reorganises its departments. Reception checks who you are once, from your room number. And your one request becomes several errands you never see. Now the most important part of the analogy: restraint. Reception does not decide the room rate. Reception does not decide what the kitchen can cook. The moment reception starts making those decisions, the hotel has two policies for one question. Remember that, because it is the most common way this pattern is ruined.

## 8. The Roles

So here are the pieces. On the outside is the client: the mobile app. It makes one call, over the slow network, to one address. In the middle is the gateway, called the product page gateway. It is the only thing that knows the page is built from four parts. Behind it, on the fast internal network, are the four services: catalog, pricing, inventory, and recommendations. Each owns its own data, and knows nothing about the page. Beside them is the sign-in service, which the gateway asks once per request. And one more piece, which does not look like a piece. The decision, made in advance, that recommendations is optional, and the other three are not.

## 9. The Gateway — and the One Catch Block

The gateway class is short, and it does four things. First, it checks the access token once, at the front door. Nothing behind it needs to ask again. Second, it calls the services it needs, over the fast internal network. About ten milliseconds each, instead of two hundred. Third, it returns one object, shaped exactly as the page wants it. Fourth, and most interesting, there is exactly one try and catch in the class. It is wrapped around one call only: recommendations. If that service does not answer, the page is served without suggestions. Why not wrap all four calls? Because losing the suggestions costs the shopper nothing. But losing the price would mean a product page with no price. That is worse than an honest error. And notice the restraint. The gateway does not change prices, apply discounts, or decide what may be sold. It only joins, and forwards.

## 10. The Same Outage, Both Ways

Now the same outage, twice, as a timeline. Without a gateway. The name arrives at two hundred milliseconds. The price at four hundred. The stock at six hundred. Then, at eight hundred, the recommendations service fails to answer. Everything that arrived is thrown away. Three correct answers lost, because the fourth was missing. Eight hundred milliseconds, to end up with nothing. With a gateway. The token is checked at one hundred milliseconds. Catalog, pricing, and inventory answer quickly, over the internal network. At one hundred and forty, recommendations fails, just as before. And the gateway serves the page anyway. Name, price, and stock, with no suggestions, in two hundred and forty milliseconds. From the shopper's point of view, nothing is wrong.

## 11. The Tests — Asserting the Cost, Not the Page

The project has twenty-five tests. And what they check is the point. No test checks that the product page is correct. Both versions build the same page, so that would prove nothing. Instead, every test checks something only the gateway gives you. The phone makes one call, not four. The token is checked once, not four times. The page arrives in two hundred and forty milliseconds, instead of eight hundred. One test exists only to block a future mistake. It checks that the price on the page is exactly the pricing service's answer, unchanged. The day someone adds a discount inside the gateway, that test fails.

## 12. Running It — Five Acts

Let's run the demo, which has five parts. Part one: no gateway. Four round trips, four token checks, and eight hundred milliseconds. Part two: with a gateway. One round trip, one token check, two hundred and forty milliseconds, and the same page. Parts three and four are the outage we just heard. The whole page lost without a gateway, and the page served minus one row with it. Part five is the one most people get wrong. This time, the catalog service is down. That is the service that knows the product's name. And the gateway does not carry on. It refuses, and tells the shopper the page cannot be shown right now. That is correct. A product page with no product on it is not a partial page. It is a blank one. A gateway is not a machine for hiding failures. It is where someone has decided, service by service, what each failure costs.

## 13. What to Remember

So, what should you remember? An A P I gateway is one front door. One trip across the network, one token check, one address, and one place that owns the decision about failures. People often ask how this differs from the Facade pattern. The shape is the same. A facade is one door in front of many classes, inside one program. A gateway is one door in front of many services, across a network that can be slow, and can fail. One variation worth knowing: Backends for Frontends. If the phone app and the in-store till want very different pages, give each its own gateway. The same pattern, one gateway per kind of client.

## 14. The Costs, Honestly

Now the honest costs. A gateway is one more service to run, watch, and scale. Every request goes through it. So if it is slow, the whole shop is slow. And the worst outcome, which is also the most common, is a gateway that slowly fills with business rules. A discount here, a special case there. Until it is a bottleneck that owns no data, and that nobody dares to change. Keep it to joining, and forwarding. And know when you do not need one. One client and three services, on a fast connection, may be fine without it. Reach for a gateway when the clients multiply, when the network is the slow part. Or when nobody can say what happens to a page if one service goes down.

## 15. Thanks for Watching

That's the A P I Gateway pattern. If you remember one sentence, make it this one. A gateway is one front door that joins and forwards, and the place where someone decides which failures cost a section, and which cost the page. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Move the try and catch in the gateway so it wraps all four calls. Then stop the pricing service, and look at the page. You will have turned an honest error into a page with no price on it. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
