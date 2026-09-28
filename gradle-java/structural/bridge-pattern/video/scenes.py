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
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Bridge pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] The Bridge pattern splits '
            'one tangled family of classes into two separate families. '
            '[[slnc 300]] One for what something does, and one for how it '
            'gets done. [[slnc 300]] The two are joined by a simple '
            'reference, not by inheritance. [[slnc 300]] So each side can '
            'grow without multiplying the other. [[slnc 600]] Think of a '
            'T V remote and a television. [[slnc 300]] The remote knows '
            'what you want. [[slnc 300]] The television knows how to do '
            'it. [[slnc 700]] In our online store, notifications are sent '
            'by email, text message, and push notification. [[slnc 500]] '
            'By the end, you will know why what a message says, and how '
            'it is delivered, should never live in the same class. [[slnc '
            '300]] And how to write the split yourself.'
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
            'Here is the scenario. [[slnc 400]] The store sends several '
            'kinds of notification. [[slnc 300]] Order confirmations, '
            'shipping updates, and password resets. [[slnc 500]] And '
            'there are several channels to send them on. [[slnc 300]] '
            'Email, text message, and push notification. [[slnc 500]] The '
            'rule is: every kind of notification must work on every '
            'channel.'
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
            'There are two very different jobs here. [[slnc 500]] First, '
            'what a notification says: its subject, and its body. [[slnc '
            '500]] Second, how it is delivered. [[slnc 300]] Email sends '
            'it unchanged. [[slnc 300]] A text message must cut long '
            'messages short. [[slnc 300]] A push notification drops the '
            'body, and shows only the subject. [[slnc 600]] Done naively, '
            'one class does both jobs, for every combination of '
            'notification and channel.'
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
            'Here is the naive approach. [[slnc 400]] One class handles '
            'order confirmations sent by text message. [[slnc 300]] It '
            'writes its own subject and body. [[slnc 300]] Then it cuts '
            'the text at a hundred and forty characters, the text message '
            'limit. [[slnc 600]] And here is the problem. [[slnc 300]] '
            'Separate classes for order confirmation by email, shipping '
            'update by email, and shipping update by text message all '
            'repeat the same shape. [[slnc 300]] And the '
            'hundred-and-forty-character rule is copied into every text '
            'message class.'
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
            'That does real damage as the system grows. [[slnc 500]] '
            'Three kinds of notification, times three channels, means '
            'nine classes. [[slnc 300]] Add a new channel, and you write '
            'one class for every kind of notification. [[slnc 300]] Add a '
            'new kind of notification, and you write one for every '
            'channel. [[slnc 600]] The text message rule is copied into '
            'every text message class. [[slnc 300]] Fix a bug in it, and '
            'you must find every copy. [[slnc 500]] What a message says, '
            'and how it is sent, are welded together. [[slnc 300]] '
            'Neither can change without touching the other.'
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
            'The Bridge pattern fixes exactly this. [[slnc 400]] The '
            'classic book on design patterns, by the authors known as the '
            'Gang of Four, describes it like this. [[slnc 300]] Separate '
            'an abstraction from its implementation, so the two can vary '
            'independently. [[slnc 600]] In plain words: two small '
            'families of classes, connected by one field. [[slnc 300]] '
            'Not by inheritance, and not by one giant class doing '
            'everything.'
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
            'Here is how to remember it. [[slnc 300]] Think of a T V '
            'remote, and a television. [[slnc 500]] The remote knows the '
            'high-level actions: volume up, next channel, power. [[slnc '
            '300]] The television knows how to actually change its own '
            'volume, on its own hardware. [[slnc 500]] Any remote works '
            'with any television that understands the same signal. [[slnc '
            '300]] And a maker can redesign the television completely, '
            'without changing what a single button means. [[slnc 600]] '
            'Two families, one connection, and each can change on its '
            'own.'
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="The Four Roles",
        body=None,
        narration=(
            'Every bridge has four roles. [[slnc 500]] The abstraction: a '
            'notification. [[slnc 300]] It knows what to say, and holds a '
            'reference to a channel. [[slnc 400]] The implementor: the '
            'message channel, a shared interface every channel follows. '
            '[[slnc 400]] Refined abstractions, like the order '
            'confirmation notification. [[slnc 300]] They add content, '
            'but never delivery logic. [[slnc 400]] And concrete '
            'implementors, like the email channel and the text message '
            'channel. [[slnc 300]] They add delivery logic, but never '
            'know what content they carry. [[slnc 600]] Here is the most '
            'important idea in this video. [[slnc 300]] A notification '
            'holds its channel as a plain field. [[slnc 300]] Not through '
            'inheritance. [[slnc 300]] That one field is the whole '
            'bridge.'
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
            'Here is the abstraction: the notification class. [[slnc '
            '400]] It holds a message channel, set once when it is '
            'created. [[slnc 500]] Its send method is fixed. [[slnc 300]] '
            'No kind of notification can change how sending works. [[slnc '
            '500]] Send asks the notification for its subject and body. '
            '[[slnc 300]] Then it hands both straight to the channel. '
            '[[slnc 300]] It never checks whether the channel is email, '
            'text message, or push. [[slnc 300]] It does not need to.'
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
            'Here is one concrete implementor: the text message channel. '
            '[[slnc 400]] The hundred-and-forty-character rule is written '
            'exactly once, right here. [[slnc 600]] Every kind of '
            'notification sent by text message gets that rule for free. '
            '[[slnc 300]] Because they all use this one channel. [[slnc '
            '300]] Fix the limit here, and every kind of notification '
            'gets the fix automatically.'
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
            'Here is a refined abstraction: the order confirmation '
            'notification. [[slnc 400]] It writes the subject and the '
            'body of the message. [[slnc 300]] Nothing here mentions '
            'email, text messages, or push. [[slnc 600]] Adding a new '
            'kind of notification, like a back-in-stock alert, costs '
            'exactly one new class like this. [[slnc 300]] And it works '
            'with every channel that already exists.'
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
            'Here is the code that ties it all together. [[slnc 400]] The '
            'same order confirmation goes out through three different '
            'channels. [[slnc 300]] Just by passing a different channel '
            'when it is created. [[slnc 600]] And the last line is the '
            'best part. [[slnc 300]] A password reset, a brand new kind '
            'of notification, already works with the same email channel. '
            '[[slnc 300]] No new channel code needed. [[slnc 300]] That '
            'is the whole payoff.'
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
            "Let's run the project. [[slnc 400]] The same order "
            'confirmation goes out over three channels. [[slnc 300]] '
            'Email and push both deliver it. [[slnc 300]] And so does the '
            'text message, because this message is short enough. [[slnc '
            '600]] Then a longer shipping update. [[slnc 300]] By email, '
            'it arrives unchanged. [[slnc 300]] By text message, it is '
            'cut off, right at the hundred-and-forty-character mark. '
            '[[slnc 500]] The same content, two different results, '
            'decided entirely by the channel.'
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
            'So, to recap. [[slnc 400]] Use a bridge when two things vary '
            'independently. [[slnc 300]] And you do not want a class for '
            'every combination. [[slnc 600]] Keep the notification side '
            "unaware of each channel's quirks. [[slnc 300]] If a kind of "
            "notification ever needs to know a channel's details to do "
            'its job, the bridge is leaking. [[slnc 600]] And one '
            'comparison worth knowing. [[slnc 300]] The Adapter pattern '
            'fixes two interfaces that already exist, and disagree. '
            '[[slnc 300]] A bridge designs two families from the start, '
            'so they only ever meet at one point.'
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
            "That's the Bridge pattern. [[slnc 400]] If you remember one "
            'sentence, make it this one. [[slnc 300]] Split what '
            'something does from how it is done, and join them with one '
            'field, so each side can grow on its own. [[slnc 500]] The '
            'full source code, written notes, diagrams, and an animated '
            'walkthrough are all in the repository. [[slnc 300]] It runs '
            'offline, with nothing installed except a Java development '
            'kit. [[slnc 500]] Here is one exercise to try. [[slnc 300]] '
            'Add a back-in-stock alert. [[slnc 300]] And check that it '
            'works on all three channels, with no other change. [[slnc '
            '500]] If this helped, a like really does help other people '
            "find it. [[slnc 300]] And subscribe, if you'd like the rest "
            'of the series. [[slnc 400]] Thanks for watching.'
        ),
    ),
]
