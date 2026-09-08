"""Scene definitions for the Bridge pattern teaching video.

Each scene has:
  key        - short id, used for the generated file names
  title      - slide heading
  kind       - "poster" | "bullets" | "code" | "console" | "quote" | "diagram" | "outro"
  body       - content, meaning depends on kind
  narration  - the text spoken by the narrator (see narration.md)
"""

SCENES = [
    # The poster is also the YouTube thumbnail, so it is the first frame of
    # the video and is saved separately as poster.png by build_video.sh.
    dict(
        key="01-poster",
        kind="poster",
        title="The Bridge Pattern",
        body=None,
        narration=(
            "Hello, and welcome. This video explains the Bridge pattern in Java, "
            "and it is written and presented by Jayasekhar Konduru. [[slnc 300]] "
            "Let's start with the simple definition. The bridge pattern takes one "
            "tangled hierarchy and splits it into two that can vary independently "
            "— what something does, and how it gets done — then joins them with a "
            "reference rather than with inheritance. Each side can then grow "
            "without multiplying the other. [[slnc 350]] That's the idea in a "
            "sentence. The rest of the video does it properly, by building a real "
            "working Java project: a notification system for an online store that "
            "sends messages over email, S M S and push. [[slnc 250]] By the end "
            "you'll know why what a message says and how it gets delivered should "
            "never live in the same class hierarchy, and how to write the split "
            "yourself."
        ),
    ),
    dict(
        key="02-scenario",
        kind="bullets",
        title="The Scenario",
        body=[
            "An online store needs to send several kinds of notification:",
            "",
            "  Order confirmations, shipping updates, password resets",
            "",
            "over several channels:",
            "",
            "  Email, SMS, push",
            "",
            "Every notification type must be sendable over every channel.",
        ],
        narration=(
            "So, imagine the notification system for an online store. "
            "[[slnc 250]] There are several kinds of notification: order "
            "confirmations, shipping updates, password resets. And there are "
            "several channels they can go out on: email, S M S, and push. "
            "[[slnc 300]] And here's the requirement. Every kind of "
            "notification needs to be sendable over every channel."
        ),
    ),
    dict(
        key="03-anatomy",
        kind="bullets",
        title="Two Very Different Things, Tangled Together",
        body=[
            "What a notification says       — its subject and body.",
            "How it gets delivered          — email, SMS truncation,",
            "                                  push dropping the body.",
            "",
            "Naively, one class has to do both, per combination.",
        ],
        narration=(
            "Look closely and there are two completely different concerns "
            "here. [[slnc 250]] What a notification says — its subject and "
            "its body. And how it physically gets delivered — email sends it "
            "unchanged, S M S has to truncate long messages, push drops the "
            "body entirely and shows only the subject. [[slnc 300]] Naively, "
            "one class ends up doing both of those jobs, for every single "
            "combination of notification type and channel."
        ),
    ),
    dict(
        key="04-problem",
        kind="code",
        title="The Naive Approach — One Class Per (Notification, Channel)",
        body="""public final class NaiveOrderConfirmationSms {
    public void send(String recipient) {
        String subject = "Order " + orderId + " confirmed";
        String body = "Your order " + orderId
                + " totalling $" + total + " has been confirmed.";
        String text = subject + ": " + body;
        if (text.length() > 140) {
            text = text.substring(0, 139) + "…";
        }
        System.out.println("[SMS to " + recipient + "] " + text);
    }
}

//  NaiveOrderConfirmationEmail, NaiveShippingUpdateEmail, and
//  NaiveShippingUpdateSms each repeat this shape independently.""",
        narration=(
            "So here's the naive approach. [[slnc 250]] "
            "NaiveOrderConfirmationSms composes its own subject and body, "
            "then truncates the combined text at 140 characters, because "
            "that's the S M S limit. [[slnc 300]] And here's the problem. "
            "NaiveOrderConfirmationEmail, NaiveShippingUpdateEmail, and "
            "NaiveShippingUpdateSms each repeat this exact shape "
            "independently — and that 140 character truncation rule gets "
            "copy-pasted into every single S M S class."
        ),
    ),
    dict(
        key="05-why-hurts",
        kind="bullets",
        title="Why That Hurts",
        body=[
            "✗   N notification types × M channels = N × M classes",
            "✗   Add Push? Two new classes. Add PasswordReset? Three more.",
            "✗   The SMS truncation rule is copy-pasted into every SMS class",
            "✗   Content and delivery are welded together in every class",
        ],
        narration=(
            "And that does real damage as the system grows. [[slnc 250]] N "
            "notification types times M channels is N times M classes. Add "
            "Push as a third channel and you write two more classes. Add "
            "PasswordReset as a third notification type and you write three "
            "more. [[slnc 300]] The S M S truncation rule is copy-pasted into "
            "every single S M S class that exists. Fix a bug in it, and you "
            "have to find every copy. [[slnc 250]] Content and delivery are "
            "welded together in every class — neither can change without "
            "touching the other."
        ),
    ),
    dict(
        key="06-pattern",
        kind="quote",
        title="The Bridge Pattern",
        body=[
            "“Decouples an abstraction from its implementation so",
            "that the two can vary independently.”",
            "",
            "—  Gang of Four, Design Patterns",
            "",
            "In plain language:",
            "two small hierarchies, connected by one field.",
        ],
        narration=(
            "The bridge pattern fixes exactly this. [[slnc 250]] In Gang of "
            "Four terms, bridge decouples an abstraction from its "
            "implementation, so that the two can vary independently. "
            "[[slnc 300]] In plain language? Two small hierarchies, "
            "connected by one field — not by inheritance, not by one giant "
            "class trying to do everything."
        ),
    ),
    dict(
        key="07-remote",
        kind="bullets",
        title="Remember It With a TV Remote",
        body=[
            "A remote knows: volume up, channel up, power.",
            "A television knows how to actually change its own volume.",
            "",
            "Any remote works with any television speaking the same signal.",
            "Redesign the television's internals — the remote doesn't change.",
            "",
            "Two hierarchies. One wire. Independent variation.",
        ],
        narration=(
            "Here's how to remember it forever. Think about a T V remote and "
            "a television. [[slnc 250]] The remote knows high-level actions: "
            "volume up, channel up, power. The television knows how to "
            "actually change its own volume on its own hardware. [[slnc 300]] "
            "Any remote works with any television that speaks the same "
            "signal, and a manufacturer can redesign the television "
            "completely without changing what a single button on the remote "
            "means. [[slnc 250]] Two hierarchies, one wire, and both vary "
            "independently."
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="The Four Roles",
        body=None,
        narration=(
            "Every bridge setup has four roles. [[slnc 200]] The "
            "abstraction, Notification, which knows what to say and holds a "
            "reference to the implementor. The implementor, MessageChannel, "
            "the shared interface every channel implements. Refined "
            "abstractions like OrderConfirmationNotification, which add "
            "content but never delivery logic. And concrete implementors "
            "like EmailChannel and SmsChannel, which add delivery logic but "
            "never know what content they're carrying. [[slnc 350]] Here's "
            "the single most important idea in this whole video. Notification "
            "holds a MessageChannel by composition, as a plain field — not by "
            "inheritance. That one field is the entire bridge."
        ),
    ),
    dict(
        key="09-abstraction",
        kind="code",
        title="The Abstraction — Notification Holds, and Delegates",
        body="""public abstract class Notification {

    private final MessageChannel channel;

    protected Notification(MessageChannel channel) {
        this.channel = channel;
    }

    public final void send(String recipient) {
        channel.deliver(recipient, subject(), body());
    }

    protected abstract String subject();
    protected abstract String body();
}""",
        narration=(
            "This is the abstraction, Notification. [[slnc 250]] It holds a "
            "MessageChannel field, assigned once in the constructor. send is "
            "final — every subclass gets delivery for free, and none of them "
            "can override how it works. [[slnc 300]] send calls subject and "
            "body on itself, then hands both strings straight to "
            "channel.deliver. It never checks whether channel is email, S M "
            "S, or push. It doesn't need to."
        ),
    ),
    dict(
        key="10-implementor",
        kind="code",
        title="A Concrete Implementor — SmsChannel Owns Its Own Rule",
        body="""public final class SmsChannel implements MessageChannel {

    static final int MAX_LENGTH = 140;

    @Override
    public void deliver(String recipient, String subject, String body) {
        String text = subject + ": " + body;
        if (text.length() > MAX_LENGTH) {
            text = text.substring(0, MAX_LENGTH - 1) + "…";
        }
        System.out.println("[SMS to " + recipient + "] " + text);
    }
}""",
        narration=(
            "And this is a concrete implementor, SmsChannel. [[slnc 250]] "
            "The 140 character truncation rule is written exactly once, "
            "right here. [[slnc 300]] Every notification type that goes out "
            "over S M S — today's three, and any added later — gets that "
            "rule for free, because they all share this one SmsChannel "
            "instance. Fix the limit here, and every notification type "
            "inherits the fix, automatically."
        ),
    ),
    dict(
        key="11-refined",
        kind="code",
        title="A Refined Abstraction — Content, Never Delivery",
        body="""public final class OrderConfirmationNotification extends Notification {

    private final String orderId;
    private final BigDecimal total;

    @Override
    protected String subject() {
        return "Order " + orderId + " confirmed";
    }

    @Override
    protected String body() {
        return "Your order " + orderId
                + " totalling $" + total + " has been confirmed.";
    }
}""",
        narration=(
            "This is a refined abstraction, "
            "OrderConfirmationNotification. [[slnc 250]] subject and body "
            "compose the message content. Nothing here mentions email, S M "
            "S, or push. [[slnc 300]] Adding a fourth notification type — "
            "say, a back-in-stock alert — costs exactly one new class like "
            "this one, and it automatically works with every channel that "
            "already exists."
        ),
    ),
    dict(
        key="12-client",
        kind="code",
        title="The Client — Mix and Match, Freely",
        body="""MessageChannel email = new EmailChannel();
MessageChannel sms = new SmsChannel();
MessageChannel push = new PushChannel();

new OrderConfirmationNotification(email, "ORD-1042", total).send("alex@example.com");
new OrderConfirmationNotification(sms, "ORD-1042", total).send("+1-555-0142");
new OrderConfirmationNotification(push, "ORD-1042", total).send("device-9f31");

new PasswordResetNotification(email, "384920").send("alex@example.com");
//  a brand-new notification type, zero new channel code required""",
        narration=(
            "And here's the client, NotificationDemo, that ties it all "
            "together. [[slnc 250]] The exact same "
            "OrderConfirmationNotification content goes out through three "
            "different channel objects, just by passing a different "
            "constructor argument. [[slnc 300]] And look at the last line. "
            "PasswordResetNotification is a brand-new notification type, and "
            "it already works with the exact same EmailChannel — zero new "
            "channel code required. That's the whole payoff."
        ),
    ),
    dict(
        key="13-output",
        kind="console",
        title="Running It",
        body="""$ ./gradlew run

== Same notification, delivered through three different channels ==
[EMAIL to alex@example.com] Order ORD-1042 confirmed -- Your order ORD-1042 ...
[SMS to +1-555-0142] Order ORD-1042 confirmed: Your order ORD-1042 totalling ...
[PUSH to device-9f31] Order ORD-1042 confirmed

== SMS truncates; Email does not -- channel behavior, isolated from content ==
[EMAIL to alex@example.com] Shipping update for order ORD-1099 -- Order ORD-1099 ...
[SMS to +1-555-0142] Shipping update for order ORD-1099: ...expect an update within 2 b…""",
        narration=(
            "When we run the project, the same notification going out over "
            "three channels is right there in the output. [[slnc 250]] "
            "Email and push get the full order confirmation instantly, and "
            "so does S M S, because that message happens to be short "
            "enough. [[slnc 300]] But look at the last two lines. A longer "
            "shipping update comes through email completely unchanged, and "
            "through S M S it gets cut off with an ellipsis, right at the "
            "140 character mark. Same notification object's content, two "
            "completely different outcomes, decided entirely by the channel."
        ),
    ),
    dict(
        key="14-wrapup",
        kind="bullets",
        title="Wrap Up",
        body=[
            "Use bridge when two things vary independently",
            "and you don't want N × M classes to cover every combination.",
            "",
            "Keep the abstraction ignorant of implementor-specific details —",
            "if a subclass needs to know a channel's quirks, the bridge leaks.",
            "",
            "Remember one sentence:",
            "Adapter reconciles two interfaces that already disagree.",
            "Bridge designs two hierarchies so they never have to.",
        ],
        narration=(
            "So, to recap. Use bridge when two things vary independently, "
            "and you don't want an explosion of N times M classes to cover "
            "every combination. [[slnc 300]] Keep the abstraction ignorant "
            "of implementor-specific details — if a Notification subclass "
            "ever needs to know a channel's quirks to do its job, the bridge "
            "has sprung a leak. [[slnc 350]] And if you remember one "
            "sentence from today, make it this one. Adapter reconciles two "
            "interfaces that already exist and disagree. Bridge designs two "
            "hierarchies from the start so they never have to agree on more "
            "than one seam."
        ),
    ),
    dict(
        key="15-outro",
        kind="outro",
        title="Thanks for Watching",
        body=[
            "If this helped, a thumbs up and a subscribe go a long way",
            "towards keeping more videos like it coming.",
            "",
            "Full source code, notes and an animation are in the repository.",
        ],
        narration=(
            "And that's the bridge pattern. [[slnc 300]] If you got "
            "something out of this, do give it a thumbs up, and subscribe. It "
            "genuinely helps the channel, and it's what makes more of these "
            "possible. [[slnc 250]] And if there's a pattern you'd like me to "
            "cover next, drop it in the comments. I read every one. [[slnc "
            "250]] All the source code, the written notes and an interactive "
            "animation are in the repository. Thanks for watching, and I'll "
            "see you in the next one."
        ),
    ),
]
