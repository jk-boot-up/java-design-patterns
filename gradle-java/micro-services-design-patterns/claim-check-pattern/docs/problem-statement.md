# Problem Statement

## The scenario

When an order ships, the store sends the invoice, a five thousand byte PDF, to the mailing service through a message broker. The broker allows messages of a thousand bytes.

## The naive version

Put the whole invoice in the message. It is the obvious way, and the broker will not take it.

```
  the invoice is 5000 bytes. message of 5000 bytes is over the broker's limit of 1000.
  most brokers cap the size of a message, and the ones that do not get slow when messages are large.
```

## What this project must deliver

A broker with a size limit; a blob store with expiry on a clock the demo controls; a claim that carries an id, a size and a checksum; a sender and a receiver that use it; bytes carried with and without; uncollected blobs swept; a tampered blob refused; the storage cost of one invoice; guessable and unguessable claims; and a plain verdict.
