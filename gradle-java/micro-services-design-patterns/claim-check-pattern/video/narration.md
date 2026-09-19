# Claim Check Pattern — Video Narration Script

## 1. Claim Check

Hello, and welcome. This video explains the Claim Check pattern in Java, and it is written and presented by Jayasekhar Konduru. The plain definition: a claim check stores a large payload somewhere cheap, and sends only a small ticket through the message broker. The receiver redeems the ticket for the payload, the way you collect a coat. This is another project in the microservices category, whose subject is how many small services stay reliable when they talk to each other. In our online store, the big thing is an invoice PDF that has to be sent to another service. By the end you will see a broker refuse a big message, see a ticket carry it instead, see how little the broker carries, see luggage nobody collected, see a changed payload caught by a checksum, and see the bill, which is extra steps and a ticket that must be hard to guess.

## 2. The Scenario

Here is the scenario. When an order ships, the online store sends the invoice, a PDF of five thousand bytes, to the mailing service through a message broker. The broker accepts messages of a thousand bytes. The question: what do we send?

## 3. A Message That Is Too Big

First, a message that is too big. The invoice is five thousand bytes, and the broker refuses it: it is over its limit of a thousand. Most brokers cap the size of a message, and the ones that do not get slow when the messages are large.

## 4. The Pattern

The pattern. Store the big thing somewhere cheap. Send a small ticket through the broker: where it is, how big it is, and a checksum. The receiver redeems the ticket, checks that it is the right thing, and then lets the storage go.

## 5. Send The Ticket, Not The Luggage

Second, send the ticket, not the luggage. The invoice goes into storage. The message carries a claim: an identifier, the size, and a checksum. The receiver redeems the claim, and gets five thousand bytes, identical to what was sent.

## 6. What The Broker Carries

Third, what the broker carries. A hundred invoices of five thousand bytes. Through a broker with no size limit: five hundred thousand bytes. By claim: five thousand nine hundred. The broker moves a small ticket. The storage holds the luggage.

## 7. Luggage Nobody Collected

Fourth, luggage nobody collected. Ten are sent, and six are collected and deleted. Four blobs are still in storage. After the time limit, a sweep removes them. And a slow receiver, arriving later with its claim, finds its blob gone. The storage needs a life span, and the receiver has to cope with a claim that expired.

## 8. Is It The Same Luggage?

Fifth, is it the same luggage? One byte is changed in storage. The receiver checks the checksum that came in the claim, and refuses the payload. The checksum in the claim is what makes a ticket for a blob safe to trust.

## 9. The Bill

Last, the bill. One invoice now takes three storage operations and two broker steps, where it took one. Claims that count up let anyone holding one read the next: blob one reads blob two's invoice. Random claims do not: a hundred thousand guesses found none. And storing then sending can stop between the two, leaving luggage nobody has a ticket for.

## 10. How To Recognise It

How do you recognise this in code you did not write? A message that holds a URL or an id and a size instead of the data. An S3 or blob storage path in an SQS or Kafka message. A ClaimCheck or Payload class in an integration library. A lifecycle rule that deletes objects after a number of days.

## 11. The Verdict

Here is my verdict, plainly. Use a claim check when payloads are larger than a broker should carry, or when many consumers need only part of the message. Make the claim unguessable and carry a checksum. Give stored payloads a life span, sweep the ones nobody collected, and handle a claim that has expired. Store first, then send, and expect the orphan.

## 12. What Is Real Here

The same honest admission as everywhere in this course. Everything is plain Java. Every number quoted comes from this program's own output. Nothing depends on a clock, so every run is the same.

## 13. When This Is Too Much

So when is it too much? If payloads are small, a claim check adds two steps for nothing. If the receiver needs the data at once and storage is slow, the ticket costs more than it saves.

## 14. Thanks for Watching

That's Claim Check. If you take one sentence away, take this one: a claim check keeps the broker light, and the price is extra steps, expiry, and a ticket that must be unguessable and verified. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository, running offline with nothing installed but a Java development kit. If you try one exercise, make the sender delete the blob if publishing the claim fails, and prove it with a broker that refuses. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
