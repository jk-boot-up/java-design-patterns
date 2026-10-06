# Claim Check Pattern — Video Narration Script

## 1. Claim Check

Hello, and welcome. This video explains the Claim Check pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A claim check stores a large item somewhere cheap. Then it sends only a small ticket through the message system. The receiver hands in the ticket, and collects the item. Think of a cloakroom at a theatre. You leave your heavy coat at the counter, and get a small numbered ticket. You carry the ticket, not the coat. Later, you hand in the ticket, and get your coat back. In our online store, the big item is an invoice P D F, which must go to another service. By the end, you will hear the message system refuse a big message. A ticket carry it instead. Items that nobody collected. A changed item caught by a check. And the bill.

## 2. The Scenario

Here is the scenario. When an order ships, the store sends the invoice to the mailing service. The invoice is a P D F of five thousand bytes. It travels through a message broker. A broker is a separate program that carries messages between services. And this broker only accepts messages up to a thousand bytes. So here is the question. What do we send?

## 3. A Message That Is Too Big

First demo: a message that is too big. The invoice is five thousand bytes. The broker's limit is a thousand. So the broker refuses it. Most brokers limit the size of a message. And the ones with no limit get slow when messages are large.

## 4. The Pattern

Now, the pattern. Store the big item somewhere cheap. Send a small ticket through the broker. The ticket says where the item is, how big it is, and carries a checksum. A checksum is a short fingerprint of the data, used to check it has not changed. The receiver hands in the ticket, and gets the item. It checks that the item matches the fingerprint. And then the storage can let it go.

## 5. Send The Ticket, Not The Luggage

Second demo: send the ticket, not the luggage. The invoice goes into storage. The message carries a claim. It holds an identifier, the size, five thousand bytes, and a checksum. The receiver hands in the claim. And gets back five thousand bytes, identical to what was sent.

## 6. What The Broker Carries

Third demo: how much the broker carries. A hundred invoices, of five thousand bytes each. Through a broker with no size limit, that is five hundred thousand bytes. With claim checks, it is five thousand nine hundred bytes. The broker carries small tickets. The storage holds the luggage.

## 7. Luggage Nobody Collected

Fourth demo: luggage nobody collected. Ten invoices are sent. Six are collected, and deleted. So four are still sitting in storage. After a time limit, a clean-up removes them. Then a slow receiver arrives, with its claim. And it finds that its invoice has gone. So stored items need a life span. And the receiver must cope with a claim that has expired.

## 8. Is It The Same Luggage?

Fifth demo: is it the same luggage? One byte of the invoice is changed, while it sits in storage. The receiver compares it with the checksum that came in the claim. They do not match, so the receiver refuses it. The checksum in the claim is what makes the stored item safe to trust.

## 9. The Bill

Finally, the bill. One invoice now takes three storage steps and two broker steps. Before, it took one. Next, the ticket numbers. If claims simply count up, one, two, three, anyone holding one can guess the next. In the demo, the holder of claim one reads the invoice for claim two. With random claims, a hundred thousand guesses found nothing. And last, storing and then sending are two separate steps. If the program stops between them, the invoice sits in storage, and nobody has a ticket for it.

## 10. How To Recognise It

How can you spot this pattern in code someone else wrote? Look for a message that holds a link or an I D and a size, instead of the data itself. Look for a storage path, such as an Amazon S3 location, inside a queue message. Look for a class called claim check, or payload, in an integration library. Or a storage rule that deletes files after a number of days.

## 11. The Verdict

So, here is the verdict. Use a claim check when items are bigger than a broker should carry. Or when many receivers need only part of the message. Make the claim impossible to guess, and include a checksum. Give stored items a life span. Clean up the ones nobody collected. And handle a claim that has expired. Store first, then send. And expect the occasional item with no ticket.

## 12. What Is Real Here

A quick, honest note about this demo. Everything is plain Java. Every number you heard comes from the program's own output. Nothing depends on a real clock, so every run gives the same result.

## 13. When This Is Too Much

So, when is this too much? If the messages are small, a claim check adds two steps for nothing. And if the receiver needs the data at once, and storage is slow, the ticket costs more than it saves.

## 14. Thanks for Watching

That's the Claim Check pattern. If you remember one sentence, make it this one. A claim check keeps the broker light, and the price is extra steps, expiry, and a ticket that must be impossible to guess, and checked. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Make the sender delete the stored invoice if sending the claim fails. Then prove it works, with a broker that refuses. If you found this useful, a like really helps other people discover it. Kindly subscribe to the channel. It helps the channel grow and bring you more content. Thanks for watching!
