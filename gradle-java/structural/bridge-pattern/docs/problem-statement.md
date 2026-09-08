# Problem Statement

## The Scenario

You are building the notification system for an online store. There are
several *kinds* of notification — order confirmations, shipping updates,
password resets — and several *channels* they can go out on — email, SMS,
push. Every kind of notification needs to be sendable over every channel.

## Attempt One: One Class Per (Notification, Channel) Pair

The obvious shape: for every notification type, write one class per
channel it can be sent through.

```java
public final class NaiveOrderConfirmationEmail {
    public void send(String recipient) {
        String subject = "Order " + orderId + " confirmed";
        String body = "Your order " + orderId + " totalling $" + total + " has been confirmed.";
        System.out.println("[EMAIL to " + recipient + "] " + subject + " -- " + body);
    }
}

public final class NaiveOrderConfirmationSms {
    public void send(String recipient) {
        String subject = "Order " + orderId + " confirmed";
        String body = "Your order " + orderId + " totalling $" + total + " has been confirmed.";
        String text = subject + ": " + body;
        if (text.length() > 140) {
            text = text.substring(0, 139) + "…";
        }
        System.out.println("[SMS to " + recipient + "] " + text);
    }
}
```

Two notification types, two channels, and already four classes:
`NaiveOrderConfirmationEmail`, `NaiveOrderConfirmationSms`,
`NaiveShippingUpdateEmail`, `NaiveShippingUpdateSms`.

## Why That Hurts

- **The class count multiplies.** *N* notification types times *M*
  channels is *N × M* classes. Add `Push` as a third channel and you write
  two more classes. Add `PasswordReset` as a third notification type and
  you write three more. Every new type on either axis multiplies against
  every type on the other.
- **Channel behaviour gets copy-pasted.** The SMS length limit and
  truncation logic lives inside `NaiveOrderConfirmationSms` — and then
  again, identically, inside `NaiveShippingUpdateSms`. Fix a bug in how SMS
  truncates and you have to find every class that duplicated the fix.
- **Content and delivery are welded together.** Each naive class mixes two
  unrelated decisions in one method: *what the message says* and *how it
  physically goes out*. Neither decision can change without touching the
  other.
- **Nothing here is a bug.** Every naive class sends a correct message.
  The waste is structural: two independent things — the notification's
  content and the channel's delivery mechanics — are forced to vary
  together, in lockstep, one class per combination.

## The Question This Project Answers

> How do we let a notification's *content* vary independently of the
> *channel* it goes out on, so that adding one more of either doesn't
> multiply the number of classes we need?

## The Goal

Give notifications and channels **two separate, small hierarchies**,
connected by one bridge, so either side can grow without touching the
other:

```java
MessageChannel sms = new SmsChannel();

new OrderConfirmationNotification(sms, "ORD-1042", total).send("+1-555-0142");
new ShippingUpdateNotification(sms, "ORD-1042", "out for delivery").send("+1-555-0142");
```

Three notification types plus three channels is six classes total, not
nine — and a fourth channel or a fourth notification type each cost
exactly one new class, not a new class per existing counterpart.

This is precisely the problem the **Bridge** design pattern solves. See
[`bridge-pattern-explained.md`](bridge-pattern-explained.md) for how.
