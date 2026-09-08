# Bridge Pattern — Video Narration Script

The full spoken script, scene by scene. `[[slnc NNN]]` marks a pause of NNN
milliseconds, an instruction to the `say` command, not a spoken word.

## 1. 01-poster

Hello, and welcome. This video explains the Bridge pattern in Java, and it is written and presented by Jayasekhar Konduru. Let's start with the simple definition. The bridge pattern takes one tangled hierarchy and splits it into two that can vary independently — what something does, and how it gets done — then joins them with a reference rather than with inheritance. Each side can then grow without multiplying the other. That's the idea in a sentence. The rest of the video does it properly, by building a real working Java project: a notification system for an online store that sends messages over email, S M S and push. By the end you'll know why what a message says and how it gets delivered should never live in the same class hierarchy, and how to write the split yourself.

## 2. 02-scenario

So, imagine the notification system for an online store. [[slnc 250]] There are several kinds of notification: order confirmations, shipping updates, password resets. And there are several channels they can go out on: email, S M S, and push. [[slnc 300]] And here's the requirement. Every kind of notification needs to be sendable over every channel.

## 3. 03-anatomy

Look closely and there are two completely different concerns here. [[slnc 250]] What a notification says — its subject and its body. And how it physically gets delivered — email sends it unchanged, S M S has to truncate long messages, push drops the body entirely and shows only the subject. [[slnc 300]] Naively, one class ends up doing both of those jobs, for every single combination of notification type and channel.

## 4. 04-problem

So here's the naive approach. [[slnc 250]] NaiveOrderConfirmationSms composes its own subject and body, then truncates the combined text at 140 characters, because that's the S M S limit. [[slnc 300]] And here's the problem. NaiveOrderConfirmationEmail, NaiveShippingUpdateEmail, and NaiveShippingUpdateSms each repeat this exact shape independently — and that 140 character truncation rule gets copy-pasted into every single S M S class.

## 5. 05-why-hurts

And that does real damage as the system grows. [[slnc 250]] N notification types times M channels is N times M classes. Add Push as a third channel and you write two more classes. Add PasswordReset as a third notification type and you write three more. [[slnc 300]] The S M S truncation rule is copy-pasted into every single S M S class that exists. Fix a bug in it, and you have to find every copy. [[slnc 250]] Content and delivery are welded together in every class — neither can change without touching the other.

## 6. 06-pattern

The bridge pattern fixes exactly this. [[slnc 250]] In Gang of Four terms, bridge decouples an abstraction from its implementation, so that the two can vary independently. [[slnc 300]] In plain language? Two small hierarchies, connected by one field — not by inheritance, not by one giant class trying to do everything.

## 7. 07-remote

Here's how to remember it forever. Think about a T V remote and a television. [[slnc 250]] The remote knows high-level actions: volume up, channel up, power. The television knows how to actually change its own volume on its own hardware. [[slnc 300]] Any remote works with any television that speaks the same signal, and a manufacturer can redesign the television completely without changing what a single button on the remote means. [[slnc 250]] Two hierarchies, one wire, and both vary independently.

## 8. 08-roles

Every bridge setup has four roles. [[slnc 200]] The abstraction, Notification, which knows what to say and holds a reference to the implementor. The implementor, MessageChannel, the shared interface every channel implements. Refined abstractions like OrderConfirmationNotification, which add content but never delivery logic. And concrete implementors like EmailChannel and SmsChannel, which add delivery logic but never know what content they're carrying. [[slnc 350]] Here's the single most important idea in this whole video. Notification holds a MessageChannel by composition, as a plain field — not by inheritance. That one field is the entire bridge.

## 9. 09-abstraction

This is the abstraction, Notification. [[slnc 250]] It holds a MessageChannel field, assigned once in the constructor. send is final — every subclass gets delivery for free, and none of them can override how it works. [[slnc 300]] send calls subject and body on itself, then hands both strings straight to channel.deliver. It never checks whether channel is email, S M S, or push. It doesn't need to.

## 10. 10-implementor

And this is a concrete implementor, SmsChannel. [[slnc 250]] The 140 character truncation rule is written exactly once, right here. [[slnc 300]] Every notification type that goes out over S M S — today's three, and any added later — gets that rule for free, because they all share this one SmsChannel instance. Fix the limit here, and every notification type inherits the fix, automatically.

## 11. 11-refined

This is a refined abstraction, OrderConfirmationNotification. [[slnc 250]] subject and body compose the message content. Nothing here mentions email, S M S, or push. [[slnc 300]] Adding a fourth notification type — say, a back-in-stock alert — costs exactly one new class like this one, and it automatically works with every channel that already exists.

## 12. 12-client

And here's the client, NotificationDemo, that ties it all together. [[slnc 250]] The exact same OrderConfirmationNotification content goes out through three different channel objects, just by passing a different constructor argument. [[slnc 300]] And look at the last line. PasswordResetNotification is a brand-new notification type, and it already works with the exact same EmailChannel — zero new channel code required. That's the whole payoff.

## 13. 13-output

When we run the project, the same notification going out over three channels is right there in the output. [[slnc 250]] Email and push get the full order confirmation instantly, and so does S M S, because that message happens to be short enough. [[slnc 300]] But look at the last two lines. A longer shipping update comes through email completely unchanged, and through S M S it gets cut off with an ellipsis, right at the 140 character mark. Same notification object's content, two completely different outcomes, decided entirely by the channel.

## 14. 14-wrapup

So, to recap. Use bridge when two things vary independently, and you don't want an explosion of N times M classes to cover every combination. [[slnc 300]] Keep the abstraction ignorant of implementor-specific details — if a Notification subclass ever needs to know a channel's quirks to do its job, the bridge has sprung a leak. [[slnc 350]] And if you remember one sentence from today, make it this one. Adapter reconciles two interfaces that already exist and disagree. Bridge designs two hierarchies from the start so they never have to agree on more than one seam.

## 15. 15-outro

And that's the bridge pattern. [[slnc 300]] If you got something out of this, do give it a thumbs up, and subscribe. It genuinely helps the channel, and it's what makes more of these possible. [[slnc 250]] And if there's a pattern you'd like me to cover next, drop it in the comments. I read every one. [[slnc 250]] All the source code, the written notes and an interactive animation are in the repository. Thanks for watching, and I'll see you in the next one.
