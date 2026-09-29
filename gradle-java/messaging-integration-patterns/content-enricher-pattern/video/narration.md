# Content Enricher Pattern — Video Narration Script

## 1. Content Enricher

Hello, and welcome. This video explains the Content Enricher pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A content enricher takes a message that is missing some details. It looks those details up once, adds them to the message, and passes the fuller message on. So the receivers never have to look anything up themselves. Think of a post office sorting room. A letter arrives with only a family name and a street. A clerk finds the house number and the postcode in the directory, writes them on the envelope, and sends it on. The postman who delivers it never needs the directory. In this video, the domain is an online shop. When a customer pays, checkout sends a message saying an order was placed. A warehouse packs the parcel, and an email service sends a confirmation. By the end, you will hear why a thin message makes every receiver do extra work. How one enricher in the middle fixes it. What to do with an order that cannot be filled in. And what the pattern costs.

## 2. The Scenario

Here is the scenario. When a customer pays, checkout sends a short message. It holds the order number, the items, and a customer ID. An ID is just a short code that points to a customer, like C 17. Two services receive the message. The warehouse needs the delivery address. The email service needs the customer's name. Neither is in the message. So who fills in the gaps?

## 3. Act One — The thin message

First demo: the thin message. Checkout sends a message saying order one was placed, by customer C 17, for a kettle. That is all it says. No name. No address. No loyalty tier. The warehouse cannot pack a parcel without an address. And the email service cannot say hello without a name.

## 4. Act Two — Every receiver looks it up

Second demo: every receiver looks the customer up. There are three orders, and two receivers. The warehouse, and the email service. Each one calls the customer service for each order. That is six calls, for three orders. Now the customer service goes down. The warehouse stops packing. The order was fine. But the warehouse could not find out where to send it.

## 5. Act Three — The enricher

Third demo: the content enricher. It sits in the middle, between checkout and the receivers. For each order, it finds the customer once. It adds the name, Priya Shah. The address, four Mill Lane, Leeds. And the loyalty tier, gold. The message grows from fifty-nine characters to one hundred and seventeen. The enricher also remembers customers it has already found. Two of the three orders are from Priya, so there are only two calls in total. Now switch the customer service off again. The warehouse still packs. The email still goes out. Everything they need is already in the message.

## 6. Act Four — A customer who cannot be found

Fourth demo: a customer who cannot be found. Order four names customer C 99. There is no such customer. The enricher does not send the order on with an empty address. The warehouse would only find out later, with a parcel and nowhere to send it. Instead, the order goes on a problem list, with the reason: no customer C 99. A person, or a retry, can deal with it there.

## 7. Act Five — The bill

Fifth demo: the bill. The details the enricher adds are a copy, taken at one moment. After order one is enriched, Priya moves house, to York. The message still says four Mill Lane, Leeds. Sometimes that is right. The parcel goes where she asked when she ordered. Sometimes it is simply out of date. And every enriched message is bigger, for every receiver, whether that receiver needs the details or not.

## 8. The Pattern

Let's name the pattern. Put one step in the middle, between the sender and the receivers. That step takes the thin message. It looks up the missing details, once. It adds them to the message. And it passes the fuller message on. That step is the content enricher. The receivers only read.

## 9. Who Does What

Here is who does what. Order placed is the thin message from checkout. The customer directory stands in for the customer service. It knows every customer's name, address and loyalty tier. The content enricher asks the directory, and builds an enriched order. That is the same order, with the customer's details added. The warehouse and the email service only read the enriched order. They never call the customer service at all.

## 10. Where You Have Seen It

You have probably met this pattern already. Apache Camel has a step called enrich. Spring Integration has an enricher. In Kafka Streams, joining a stream of orders with a table of customers is the same idea. And an API gateway that adds a user's details to each request, after checking their login, is enriching the request.

## 11. When To Use It

So, when should you use it? Use a content enricher when several receivers need the same details, and the sender does not have them. Send any message it cannot fill in to a problem list, with the reason. And skip it for details that must be current at the moment of acting, such as stock levels or prices. For those, the receiver should ask the owning service when it acts.

## 12. Thanks for Watching

That's the Content Enricher pattern. If you remember one sentence, make it this one. When a message is too thin for its receivers, fill it in once, in the middle. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Add a third receiver, a loyalty service that needs the tier. Then count the lookups, with and without the enricher. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
