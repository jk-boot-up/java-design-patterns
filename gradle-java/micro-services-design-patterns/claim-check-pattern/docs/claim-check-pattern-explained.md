# Claim Check, Explained

## The pattern in one sentence

A claim check stores a large payload somewhere cheap and sends only a small ticket through the message broker, so the receiver can redeem the ticket for the payload.

## The six acts

### A Message That Is Too Big

The invoice is five thousand bytes, and the broker refuses it: over its limit of a thousand.

```
  the invoice is 5000 bytes. message of 5000 bytes is over the broker's limit of 1000.
  most brokers cap the size of a message, and the ones that do not get slow when messages are large.
```

### Send The Ticket, Not The Luggage

The invoice goes to storage. The message carries a claim with a 37 character id, the size and a checksum. The receiver redeems it and gets the same 5000 bytes.

```
  the invoice is stored. the message carries a claim: an id of 37 characters, size 5000, checksum 7ad4d4cb072db3a2.
  the receiver redeems it and gets 5000 bytes, identical to what was sent: true.
```

### What The Broker Carries

A hundred invoices carry five hundred thousand bytes through a broker with no limit, and five thousand nine hundred by claim.

```
  100 invoices of 5000 bytes. through a broker with no limit: 500000 bytes. by claim: 5900 bytes.
  the broker moves a small ticket. the storage holds the luggage.
```

### Luggage Nobody Collected

Ten are sent and six collected and deleted, so four blobs are left. After the time limit a sweep removes them. A slow receiver who arrives later finds its blob gone.

```
  10 sent, 6 collected and deleted. blobs still stored: 4.
  after the time limit, the sweep removes 4. stored now: 0.
  a slow receiver arrives with its claim: the blob for this claim expired or was never stored.
```

### Is It The Same Luggage?

One byte is changed in storage. The receiver checks the checksum in the claim and refuses the payload.

```
  one byte changed in storage. the receiver: the payload is not the one that was sent: the checksum does not match.
  the checksum in the claim is what makes a ticket for a blob safe to trust.
```

### The Bill

One invoice now takes three storage operations and two broker steps, where it took one. Claims that count up let anyone read the next invoice, and random ones do not. And storing then sending can stop between the two.

```
  one invoice, one way: 3 storage operations (put, get, delete) and 2 broker steps. before, there was 1.
  claims that count up: someone holding blob-1 tries blob-2 and reads: ben's invoice.
  random claims: 100000 guesses of the counting kind found 0 invoices. a claim must be hard to guess.
  storing, then sending, can stop between the two, and leave luggage nobody has a ticket for.
```

## The verdict

Use a claim check when payloads are larger than a broker should carry, or when many consumers need only part of the message. Make the claim unguessable and carry a checksum. Give stored payloads a life span, sweep the ones nobody collected, and handle a claim that has expired. Store first, then send, and expect the orphan.

## How to recognise this in code you did not write

- A message that holds a URL or an id and a size instead of the data.
- An S3 or blob storage path in an SQS or Kafka message.
- A `ClaimCheck` or `Payload` class in an integration library.
- A lifecycle rule that deletes objects after a number of days.

## Where you have already met this

Amazon SQS's extended client, Azure Service Bus with blob storage, and most systems that email attachments through a queue.

## When this is too much

If payloads are small, a claim check adds two steps for nothing. If the receiver needs the data at once and storage is slow, the ticket costs more than it saves.
