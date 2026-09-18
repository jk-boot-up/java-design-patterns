"""Scene definitions for the Externalised Configuration teaching video.

Each scene has:
  key        - short id, used for the generated file names
  title      - slide heading
  kind       - "poster" | "bullets" | "code" | "console" | "quote" | "diagram" | "outro"
  body       - content, meaning depends on kind
  narration  - the text spoken by the narrator (see narration.md)

The narration is written to stand on its own. A large share of the audience
listens rather than watches -- on a phone, in a pocket, on a commute -- so no
sentence points at the screen, the analogy is spoken in full before any class
name, and the code slides are described in words rather than read out as
syntax. The slides illustrate the narration; they never carry it.

The running order is unusual for this series and deliberately so. The pattern
itself is finished by scene 9, and scenes 10 to 15 are the bill: the outage, the
two ways a bad value fails, and the four guards that have to be rebuilt. This
pattern is easy to adopt and easy to adopt badly, and the second half is the
half that decides which.
"""

SCENES = [
    # The poster is also the YouTube thumbnail, so it is the first frame of
    # the video and is saved separately as poster.png by build_video.sh.
    dict(
        key="01-poster",
        kind="poster",
        title="Externalised Configuration",
        body=None,
        narration=(
            "Hello, and welcome. This video explains the Externalised "
            "Configuration design pattern in Java, and it is written and "
            "presented by Jayasekhar Konduru. [[slnc 300]] Let's start with the "
            "simple definition. Externalised configuration means keeping the "
            "values your program needs outside the program itself, and reading "
            "them while it runs — so that changing one of those values does not "
            "mean building and shipping a new program. [[slnc 350]] Think of the "
            "greengrocer with a chalk board outside the shop. The prices are not "
            "painted on the wall. When the tomatoes need shifting before closing, "
            "somebody walks out with a cloth and a stick of chalk, and the price "
            "is different thirty seconds later. Nobody repaints the shop. [[slnc "
            "300]] But notice the other half of that. The board is outside, where "
            "anybody can reach it — which is also why anybody can write nonsense "
            "on it. [[slnc 350]] That's the idea in a sentence. The rest of the "
            "video does it properly, by building a real working Java project: an "
            "online shop that gives free delivery to anyone spending over fifty "
            "pounds, and a marketing team who want that to be thirty-five pounds "
            "by Saturday morning. [[slnc 250]] By the end you'll know why a "
            "perfectly well-written constant can still be in the wrong place, "
            "exactly where the value has to be read from and why that one "
            "placement decision is the whole pattern, and — just as importantly — "
            "the four guards that value quietly loses on the way out of your "
            "source code, and what you have to build to get them back."
        ),
    ),
    dict(
        key="02-scenario",
        kind="bullets",
        title="The Scenario",
        body=[
            "An online shop, and one promise on the delivery page.",
            "",
            "    Spend over £50 and delivery is free.",
            "    Otherwise delivery costs £4.99.",
            "",
            "Three baskets waiting at the checkout:",
            "",
            "    ORD-7101    £62.00",
            "    ORD-7102    £48.00",
            "    ORD-7103    £31.50",
            "",
            "On Friday at 16:30, marketing want £35 by Saturday.",
        ],
        narration=(
            "So, imagine an online shop, and one promise on its delivery page. "
            "[[slnc 250]] Spend over fifty pounds and delivery is free. Spend less "
            "than that and delivery costs four pounds ninety-nine. [[slnc 300]] "
            "There are three baskets waiting at the checkout, and I want you to "
            "hold onto these three numbers, because every act of this project uses "
            "the same three. The first basket has sixty-two pounds of goods in it. "
            "The second has forty-eight pounds. The third has thirty-one pounds "
            "fifty. [[slnc 350]] Against a fifty pound threshold, the first one "
            "ships free and the other two pay. Nothing surprising. [[slnc 300]] "
            "And then on Friday afternoon, at half past four, the marketing team "
            "come to you. Sales are soft, they have a campaign going out on "
            "Saturday morning, and they would like free delivery over thirty-five "
            "pounds instead of fifty for the weekend. [[slnc 250]] It is a "
            "one-number change, and it is not a big ask. Keep that Friday half "
            "past four in mind — it is going to do a lot of work in this video."
        ),
    ),
    dict(
        key="03-problem",
        kind="code",
        title="Where the Number Lives Today",
        body="""public final class HardCodedCheckout implements Checkout {

    private static final Money FREE_DELIVERY_OVER = Money.pounds(50);
    private static final Money STANDARD_DELIVERY = Money.pence(499);
    ...
}
// Named.  Typed.  In one place.  A reviewer would pass it.
// There is nothing wrong with this line.""",
        narration=(
            "Here is where that fifty pounds lives today. It is a constant in the "
            "checkout class: private, static, final, and given a name that says "
            "exactly what it is. [[slnc 300]] Now, normally at this point in a "
            "design patterns video I would show you something bad and then rescue "
            "it. I am not going to do that, because there is nothing wrong with "
            "this line. [[slnc 350]] It is named, so it is not a magic number. It "
            "is typed as money, so it cannot accidentally be a postcode or a "
            "quantity. It appears in exactly one place, so there is no risk of two "
            "copies drifting apart. And if I put it in front of you in a code "
            "review, you would approve it without a comment. [[slnc 400]] That "
            "matters for the whole rest of this video, so let me say it plainly. "
            "This pattern does not fix bad code. What it fixes is a value that is "
            "in a place with the wrong change speed. [[slnc 300]] The code is "
            "fine. The problem is what it takes to make that fifty into a "
            "thirty-five."
        ),
    ),
    dict(
        key="04-the-cost",
        kind="console",
        title="What Changing One Number Costs",
        body="""Act 2 - marketing want £35.00 from Sat 08 Mar 09:00,
        and they ask on Friday at 16:30

  edit the constant         15 min   done Fri 07 Mar 16:45
  code review               45 min   done Mon 10 Mar 09:30
  build and test            25 min   done Mon 10 Mar 09:55
  release approval          30 min   done Mon 10 Mar 10:25
  deploy and watch          20 min   done Mon 10 Mar 10:45

  total work: 2 hours 15 minutes
  live at:    Mon 10 Mar 10:45
  the promotion was for the weekend.
  It is late by 2 days 1 hour 45 minutes.""",
        narration=(
            "So let's price it. This is the second act of the demo, and it walks "
            "the change through a release pipeline that any of you would recognise. "
            "[[slnc 300]] Editing the constant takes fifteen minutes, and it "
            "finishes at a quarter to five on Friday. Then a code review: "
            "forty-five minutes. And it finishes on Monday morning at half past "
            "nine. [[slnc 400]] Read those two lines against each other, because "
            "that gap is the whole point. The edit finished at a quarter to five on "
            "Friday and the review finished on Monday, because the release window "
            "closed at five o'clock and did not open again until Monday morning. "
            "[[slnc 350]] Then the build and the tests, twenty-five minutes. Then a "
            "release approval, half an hour. Then the deploy itself, and twenty "
            "minutes watching it to make sure nothing caught fire. [[slnc 300]] Add "
            "it up. Two hours and fifteen minutes of actual work. And it goes live "
            "on Monday at a quarter to eleven — which is two days and nearly two "
            "hours after the Saturday morning the promotion was for. The campaign "
            "runs all weekend advertising free delivery over thirty-five pounds, "
            "and the shop charges everybody as though it were fifty. [[slnc 400]] "
            "Now, here is the part I want you to sit with. Try to delete a step "
            "from that list. [[slnc 250]] Code review is how a typo does not reach "
            "a million customers. The build and the tests are how you avoid "
            "shipping something that does not compile. The approval is how a "
            "regulated business demonstrates that its releases are controlled. And "
            "the weekday window exists because the people who would notice a bad "
            "release are at their desks on weekdays — a deploy is simply not a "
            "thing you do at nine in the morning on a Saturday. [[slnc 400]] "
            "Nothing on that list is waste. Every single step is there for a good "
            "reason. And the promotion still misses its weekend. That is the "
            "problem this pattern exists to solve, and notice that it is not a code "
            "quality problem at all."
        ),
    ),
    dict(
        key="05-pattern",
        kind="quote",
        title="The Pattern",
        body=[
            "Some values are decisions about behaviour.",
            "Some values are decisions about business policy.",
            "",
            "Behaviour belongs behind the pipeline.",
            "",
            "Policy changes on somebody else's calendar,",
            "so keep it outside, and read it while you run.",
        ],
        narration=(
            "So here is the move, and it starts with a distinction rather than with "
            "any code. [[slnc 300]] Some of the values in your program are "
            "decisions about behaviour. The order of the steps in a workflow. How a "
            "total is built up. The algorithm you chose. Those belong behind the "
            "pipeline, and you should be glad they are hard to change, because the "
            "pipeline is what stops somebody breaking them. [[slnc 400]] But some "
            "values are not decisions about behaviour at all. They are decisions "
            "about business policy — a threshold, a page size, a promotion window, "
            "how long a session lasts. Those change on somebody else's calendar, "
            "and that somebody is usually not an engineer. [[slnc 350]] And here is "
            "the sentence the whole pattern rests on. Putting a policy value behind "
            "the release pipeline does not make it safer. It makes it late. [[slnc "
            "400]] So externalised configuration is the decision to keep that kind "
            "of value outside the compiled program, and to read it while the "
            "program is running. That's it. That is the pattern. [[slnc 300]] "
            "Everything else in this video — every benefit, and every one of the "
            "costs — falls out of that one sentence."
        ),
    ),
    dict(
        key="06-three-moves",
        kind="bullets",
        title="Three Moves",
        body=[
            "1.  The value comes from outside,",
            "    and it is read on every use.",
            "        Not once in the constructor. Every time.",
            "",
            "2.  The code still carries a default.",
            "        The source can be unreachable. The shop",
            "        must keep selling anyway.",
            "",
            "3.  The guards move out with the value.",
            "        The compiler, the type, the reviewer and the",
            "        history all stayed behind in the source file.",
        ],
        narration=(
            "There are three moves, and most write-ups of this pattern only give "
            "you the first two. [[slnc 350]] Move one. The value comes from "
            "outside, and — this is the part people get wrong — it is read on every "
            "single use. Not once when the object is built. Every time somebody "
            "asks. [[slnc 300]] Move two. The code still carries its own default, "
            "for the value it would have used if nobody had configured anything. "
            "Because the place the value now lives is somewhere that can be "
            "unreachable, and a shop that refuses to serve customers because a "
            "configuration server is down is a worse shop than one with the number "
            "baked in. [[slnc 400]] And move three, which is the one that gets "
            "skipped, and which the second half of this video is about. [[slnc "
            "250]] When that value was a constant in the source code, four "
            "different things were quietly protecting it. The compiler, which would "
            "refuse to build if you wrote the word fifty where a number belongs. "
            "The type system, which would not let it be anything other than money. "
            "A human reviewer, who would ask you an awkward question if you tried "
            "to set it to minus one pound. And version control, which recorded who "
            "changed it, when, and what it was before. [[slnc 400]] Not one of "
            "those four follows the value out of the source file. If you want them, "
            "you have to build them again yourself, on purpose, on the outside."
        ),
    ),
    dict(
        key="07-roles",
        kind="diagram",
        title="Who Does What",
        body=None,
        narration=(
            "Let me name the parts, because there are only five that matter and "
            "they each do one job. [[slnc 300]] There is the checkout, which is the "
            "code that needs the number. It works out whether a basket qualifies "
            "for free delivery, and that arithmetic is identical in both versions "
            "of this project. [[slnc 300]] There is the settings reader, and this "
            "is the one piece of the program that knows the outside world exists. "
            "The checkout asks it for the threshold and gets back an amount of "
            "money. It does not know, and cannot find out, whether that money came "
            "from a configuration server, from a file, or from the default baked "
            "into the code. [[slnc 400]] There is the declared setting, which is a "
            "small record holding four things: the key the value is stored under, "
            "the default to use if nothing is configured, the lowest value that "
            "makes sense, and the highest. Hold onto that little record, because it "
            "is going to turn out to be the replacement for the compiler. [[slnc "
            "350]] There is the configuration source itself, and the important "
            "thing about it is how little it does. It stores text against keys. It "
            "does not know what any of that text means, and it has no opinion about "
            "whether the text is sensible. [[slnc 350]] And there is a change log, "
            "which records every write: the key, the new value, the value it "
            "displaced, who did it, and when. That is the replacement for version "
            "control, and it is part of the pattern rather than an optional extra. "
            "[[slnc 300]] Two of these have two versions in the project, and that "
            "is the whole teaching device. There are two checkouts — one with the "
            "number in the code and one that reads it — and there are two settings "
            "readers, one that trusts whatever text it is given and one that "
            "checks it. The same bad values go through both."
        ),
    ),
    dict(
        key="08-the-read",
        kind="code",
        title="The One Line That Is the Pattern",
        body="""@Override
public DeliveryQuote quote(Basket basket) {

    SettingValue threshold = settings.money(FREE_DELIVERY_OVER);

    Money cost = basket.goodsTotal().isAtLeast(threshold.amount())
            ? Money.zero()
            : standardDelivery;

    return new DeliveryQuote(basket, cost,
            threshold.amount(), threshold.origin());
}
// The read is INSIDE quote().  Not in the constructor.""",
        narration=(
            "So here is the configured checkout, and I want you to notice how "
            "little of it is new. [[slnc 300]] It is handed a basket. It asks the "
            "settings reader for the free-delivery threshold. If the basket total "
            "is at least that threshold, delivery is free, and otherwise delivery "
            "is the standard charge. Then it hands back a quote. [[slnc 350]] The "
            "arithmetic is character for character the same as the hard-coded "
            "version. One line differs: instead of reading a constant, it asks for "
            "a setting. [[slnc 400]] And now the single most important detail in "
            "this entire video, which is not about what that line says but about "
            "where it sits. [[slnc 250]] The read happens inside the quote method. "
            "Every time a customer reaches the delivery step, the threshold is "
            "fetched again. [[slnc 350]] Every tidy-minded developer who meets this "
            "code wants to move that line into the constructor and keep the value "
            "in a field. It reads better. It looks more efficient. And it destroys "
            "the pattern — because now the only way to pick up a new value is to "
            "restart the program, and you have swapped a rebuild for a restart. "
            "Restarting a live shop on a Saturday morning is not much of a trade. "
            "[[slnc 350]] There is a test in this project called, the threshold is "
            "read every time, and its entire purpose is to fail the moment somebody "
            "helpfully tidies this up. [[slnc 300]] One last thing to notice. What "
            "comes back is not just an amount. It is an amount together with a "
            "short description of where that amount came from, and that description "
            "travels all the way out into the quote. Once a value can move, the "
            "question you get asked is no longer what the threshold is. It is which "
            "threshold was in force for this particular order, and where it came "
            "from."
        ),
    ),
    dict(
        key="09-four-seconds",
        kind="console",
        title="Four Seconds",
        body="""Act 3 - the same threshold, read on every quote

  before the change, with nothing configured:
    ORD-7101  goods £62.00  delivery FREE
    ORD-7102  goods £48.00  delivery £4.99
    ORD-7103  goods £31.50  delivery £4.99

  #1  Fri 07 Mar 16:30:04  delivery.freeOver  (not set) -> 35

  the very next quote, 4 seconds later:
    ORD-7101  goods £62.00  delivery FREE
    ORD-7102  goods £48.00  delivery FREE
    ORD-7103  goods £31.50  delivery £4.99

  No rebuild, no redeploy, no restart.""",
        narration=(
            "And this is what it buys. [[slnc 300]] The third act starts with "
            "nothing configured at all, so every quote falls back to the default "
            "compiled into the code, and the shop behaves exactly as it did in act "
            "one. The sixty-two pound basket ships free and the other two pay. That "
            "is worth pausing on: adopting this pattern, on its own, changed no "
            "behaviour whatsoever. [[slnc 400]] Then somebody in marketing types "
            "thirty-five into a box. [[slnc 250]] Four seconds later, the very next "
            "basket is quoted against the new threshold, and the forty-eight pound "
            "basket now ships free. [[slnc 350]] No rebuild. No redeploy. No "
            "restart. Nobody was paged, nobody approved anything, and no pipeline "
            "ran. [[slnc 300]] Set that four seconds against the two hours and "
            "fifteen minutes of work spread over a weekend that we priced earlier, "
            "and you have the entire commercial case for this pattern in one "
            "comparison. [[slnc 350]] That is the good news, and it is genuinely "
            "good news. The rest of the video is the bill, and it gets more room "
            "than the benefit did — because the value did not leave your source "
            "file on its own. It left four guards behind."
        ),
    ),
    dict(
        key="10-outage",
        kind="console",
        title="The Bill, Part One — When the Source Goes Away",
        body="""Act 4 - the config server stops answering

    ORD-7102  goods £48.00  delivery £4.99

  threshold in force: £50.00
  came from: the default compiled into the code,
             because the config server could not be reached

  the shop keeps selling, because the code carries
  its own default.

  note what it quietly lost, though: the promotion.
  Back to £50.00, with no error and no alarm.""",
        narration=(
            "The first item on the bill is the one everybody thinks of, and it is "
            "also the one everybody handles correctly. [[slnc 300]] The network "
            "link to the configuration source drops. Every setting falls back to "
            "the default compiled into the code, and the shop starts, and keeps "
            "selling. That is exactly why move two insisted on a default, and it is "
            "the right behaviour. [[slnc 400]] But read what it quietly lost. "
            "[[slnc 250]] The threshold is back to fifty pounds. The promotion is "
            "off. The campaign is still running, still advertising thirty-five "
            "pounds, and the shop is charging everybody as though nothing had ever "
            "been configured. [[slnc 350]] And nothing anywhere reports it. No "
            "exception reaches a customer. No log line is written. No alert fires. "
            "The shop is behaving perfectly reasonably, and it is behaving "
            "perfectly reasonably in a way that is losing the business money. "
            "[[slnc 350]] The only trace of it anywhere in the system is that "
            "little description of where the value came from, which is the second "
            "time in this video that the provenance has turned out to be worth "
            "carrying. Surviving an outage quietly is not the same thing as "
            "surviving it correctly."
        ),
    ),
    dict(
        key="11-cost-minus-one",
        kind="console",
        title="The Bill, Part Two — A Number Nobody Checked",
        body="""Act 5 - somebody types -1 into the box on Saturday morning

  #2  Sat 08 Mar 09:12:04  delivery.freeOver  35  ->  -1

    ORD-7101  goods £62.00  delivery FREE
    ORD-7102  goods £48.00  delivery FREE
    ORD-7103  goods £31.50  delivery FREE

  every basket in the shop now ships free,
  including the £31.50 one.

  -1 is a perfectly well-formed number, so nothing
  complains.  No exception.  No log line.""",
        narration=(
            "The second item on the bill is the one that should frighten you. "
            "[[slnc 300]] Saturday morning, twelve minutes past nine. Somebody "
            "types minus one into the box. Maybe they meant to type thirty-five and "
            "caught the wrong key. Maybe a form defaulted to it. It does not "
            "matter. [[slnc 350]] The configuration source stores it happily, "
            "because storing text is all a configuration source does. And then "
            "every basket in the shop is worth more than minus one pound, so every "
            "basket qualifies for free delivery — including the thirty-one pound "
            "fifty one, where the delivery costs the shop more than the margin on "
            "the order. [[slnc 400]] Now listen to what does not happen. There is "
            "no exception. There is no error log. Nothing crashes, nothing retries, "
            "no alert fires, and no dashboard turns red. [[slnc 300]] And that is "
            "not a bug in the program. Minus one is a perfectly well-formed number. "
            "The program was told the threshold is minus one pound, and it is "
            "faithfully, correctly applying it. There is nothing here to fix, "
            "because in software terms nothing is broken. [[slnc 400]] There is a "
            "test in this project that asserts this behaviour and it passes. It is "
            "not a failure waiting to be repaired. It is a description of the "
            "pattern working exactly as designed, with a value somebody typed "
            "wrongly. [[slnc 350]] The first symptom of this is the margin report, "
            "and the margin report is on Monday. It reached the running shop in "
            "four seconds, with no compiler, no code review and no test suite "
            "anywhere in the way. That is what you traded the release pipeline for."
        ),
    ),
    dict(
        key="12-cost-fifty",
        kind="console",
        title="The Bill, Part Three — Not a Number at All",
        body="""Act 6 - eight minutes later, somebody types the word fifty

  #3  Sat 08 Mar 09:20:04  delivery.freeOver  -1  ->  fifty

    ORD-7101  checkout failed: setting 'delivery.freeOver'
              has value "fifty" — expected an amount of
              money such as "35" or "4.99"
    ORD-7102  checkout failed: ...
    ORD-7103  checkout failed: ...

  not one basket can be quoted.  The shop is down,
  and it was taken down by a text box.""",
        narration=(
            "Eight minutes later, somebody tries to fix it, and types the word "
            "fifty. Not the digits. The word. [[slnc 350]] This one is not a number "
            "at all, so turning the text into money fails, an exception is thrown, "
            "nothing catches it, and it travels straight out through the checkout. "
            "[[slnc 300]] Not one basket in the shop can be quoted. Every customer "
            "at the delivery step gets an error page. The shop is down — and it was "
            "taken down by somebody typing a word into a text box, with nothing "
            "deployed and no code changed anywhere. [[slnc 400]] The compiler would "
            "have refused this. It would not have built. That is not a small "
            "difference: the compiler is no longer anywhere in the path between a "
            "person's fingers and your running shop. [[slnc 350]] And here is the "
            "uncomfortable comparison. Of those two failures, this one is the "
            "better failure. [[slnc 300]] Because you find out. Error rates spike, "
            "somebody is paged, and it is understood within minutes. Minus one runs "
            "all weekend, cheerfully, giving away delivery on every order in the "
            "shop, and the first person to notice is an accountant. [[slnc 350]] A "
            "loud failure is a bad afternoon. A quiet failure is a bad quarter."
        ),
    ),
    dict(
        key="13-guards",
        kind="bullets",
        title="The Four Guards, and What Replaces Them",
        body=[
            "The compiler refusing \"fifty\"",
            "    ->  a typed setting that parses, or rejects",
            "",
            "A reviewer querying -1",
            "    ->  a declared range the value must fall inside",
            "",
            "Version control's history",
            "    ->  an audit trail: who changed what, and when",
            "",
            "A revert and a redeploy",
            "    ->  a rollback as fast as the change was",
        ],
        narration=(
            "So let's pay the bill, item by item, because each of those four guards "
            "has a replacement and none of the replacements is difficult. [[slnc "
            "350]] The compiler refused the word fifty. Its replacement is a typed "
            "setting: something that takes the text, tries to turn it into money, "
            "and refuses it at the boundary if it cannot. [[slnc 300]] A human "
            "reviewer would have queried minus one pound. Its replacement is a "
            "declared range — a lowest value and a highest value written down as "
            "data, that the configured value must fall between. [[slnc 300]] "
            "Version control knew who changed the number, when, and what it was "
            "before. Its replacement is an audit trail that records exactly those "
            "things every time a value is written. [[slnc 300]] And a bad release "
            "was undone by a revert and a redeploy. Its replacement is a rollback "
            "that is as fast as the change was — which, once you have the audit "
            "trail, is nearly free. [[slnc 400]] Look at that list again and notice "
            "what it is not. It is not a framework, it is not a product, and it is "
            "not clever. It is four small, ordinary pieces of code. [[slnc 300]] "
            "The reason this pattern goes wrong so often in real systems is not "
            "that these are hard. It is that the first two moves work on their own, "
            "and so nobody gets round to the third."
        ),
    ),
    dict(
        key="14-validated",
        kind="console",
        title="Declared, and Validated at the Boundary",
        body="""Act 7 - declare the setting, and check at the edge

  delivery.freeOver: money, £5.00 to £200.00, default £50.00

  the word fifty is still configured.  With validation on:
    ORD-7101  goods £62.00  delivery FREE   threshold £50.00
    came from: the default compiled into the code,
               because the configured value was rejected

  #5  Sat 08 Mar 11:40:04  delivery.freeOver  35  ->  -1
    ORD-7103  goods £31.50  delivery £4.99   threshold £35.00
    came from: the last value that passed validation

  REJECTED  "fifty" — expected an amount of money
  REJECTED  "-1"    — expected between £5.00 and £200.00""",
        narration=(
            "Here are the first two of those guards, running against the same two "
            "bad values. [[slnc 350]] The setting is now declared, out loud, as "
            "four things: the key it lives under, that it holds money, that it must "
            "be between five pounds and two hundred pounds, and that it defaults to "
            "fifty pounds if nothing is configured. [[slnc 400]] Spend a moment on "
            "those two bounds, because they are the interesting part. Why five "
            "pounds at the bottom? Because below five pounds you are giving free "
            "delivery away on a packet of crisps. Why two hundred at the top? "
            "Because above two hundred pounds almost nobody qualifies, and the "
            "promotion is broken in the other direction — quietly, and nobody "
            "notices for a month. [[slnc 350]] Both of those are business "
            "judgements, not technical ones. And that is precisely why a program "
            "has to enforce them, because the person typing into the box on a "
            "Saturday morning is not thinking about either end. [[slnc 400]] Now "
            "watch what happens. The word fifty is still configured, and it is "
            "refused at the edge. The shop falls back to fifty pounds from the "
            "code, and keeps trading. Nobody sees an error page. [[slnc 300]] Then "
            "a good value, thirty-five, arrives and passes, and the reader does one "
            "more thing with it: it files it away as the last value known to be "
            "good. [[slnc 350]] And then somebody in operations types minus one "
            "again. It is refused, and look very carefully at what the shop falls "
            "back to. Not fifty pounds from the code. Thirty-five — the last value "
            "that passed. [[slnc 400]] That distinction is worth arguing about, so "
            "let me make the case. Somebody deliberately set that promotion to "
            "thirty-five pounds an hour ago. If an unrelated typo silently reverted "
            "it to fifty, you would have cancelled a promotion that nobody decided "
            "to cancel — and you would have done it in the name of safety. Keeping "
            "the last good value keeps the last actual decision. [[slnc 350]] And "
            "notice the last two lines. Both rejections are recorded, loudly. A "
            "guard that swallows bad input in silence is only half a guard, because "
            "the typo is still sitting in the configuration, the promotion still is "
            "not what anybody intended, and nobody is looking for it."
        ),
    ),
    dict(
        key="15-trail-rollback",
        kind="console",
        title="The Trail, and a Rollback in Four Seconds",
        body="""Act 8 - who changed what, and when

  #1  Fri 07 Mar 16:30:04  (not set) -> 35     by marketing
  #2  Sat 08 Mar 09:12:04  35        -> -1     by marketing
  #3  Sat 08 Mar 09:20:04  -1        -> fifty  by marketing
  #4  Sat 08 Mar 10:05:04  fifty     -> 35     by marketing
  #5  Sat 08 Mar 11:40:04  35        -> -1     by ops

  5 changes to one setting in under a day, and not one
  of them is in the git history.

Act 9 - a rollback as fast as the change

  #6  Sat 08 Mar 11:40:08  -1  ->  35  by on-call (rollback)

  nobody had to remember the old value: the log had it.
  the same fix through the pipeline: live Mon 10 Mar 11:15.""",
        narration=(
            "And here are the other two guards. [[slnc 300]] This is every change "
            "made to that one setting: five of them, in under a day, and each one "
            "records the key, the new value, the value it displaced, who did it, and "
            "the second it happened. [[slnc 350]] Now read the line under the list, "
            "because it is the whole justification for building this. Five changes "
            "to a business-critical number in a single day, and not one of them is "
            "in the version control history. [[slnc 300]] When that value left the "
            "source code, it left version control behind, and this list is the "
            "replacement. [[slnc 350]] And the reason you need it is not the "
            "question you expect. Nobody will ever ring you up to ask what the "
            "threshold is now — you can look at the box. The question you actually "
            "get asked, three weeks later, by somebody investigating a complaint, "
            "is what the threshold was at nine o'clock on Saturday morning. Without "
            "this list, there is no honest answer to that. [[slnc 400]] And then the "
            "fourth guard, which is my favourite, because it has no equivalent at "
            "all in the source-code world. [[slnc 250]] Saturday, twenty to twelve. "
            "The margin report looks wrong, somebody on call works out that the "
            "threshold is minus one pound, and rolls it back. Four seconds after the "
            "decision, the shop is quoting on thirty-five pounds again. [[slnc "
            "350]] And nobody had to remember that it used to be thirty-five. "
            "Nobody had to guess, at speed, on a Saturday, while the shop gave "
            "delivery away. The log had it, because every entry records the value it "
            "displaced, so the rollback is a lookup rather than an act of memory. "
            "[[slnc 400]] Compare that with the alternative. The same correction "
            "through the release pipeline would have been live on Monday at a "
            "quarter past eleven. [[slnc 300]] A bad release takes a release to "
            "undo. A bad value takes four seconds. [[slnc 350]] That is the line I "
            "would want you to take away, because it turns the whole argument round. "
            "Externalised configuration is not a way of avoiding governance. It is a "
            "way of governing a change in seconds instead of days."
        ),
    ),
    dict(
        key="16-boundary",
        kind="bullets",
        title="What to Externalise, and What Never To",
        body=[
            "Ask two questions, in this order.",
            "",
            "    Does this value change on an engineering",
            "    calendar, or on somebody else's?",
            "",
            "    What can I break by typing into that box?",
            "",
            "A threshold, a page size, a timeout  ->  externalise.",
            "The order of the steps, the shape of a total,",
            "the algorithm  ->  leave it in the code.",
            "",
            "Not the same thing as a feature flag:",
            "a parameter lives forever, a switch is meant to die.",
        ],
        narration=(
            "So, what should you actually externalise? There are two questions, and "
            "the order matters. [[slnc 350]] The first one is: does this value "
            "change on an engineering calendar, or on somebody else's? A free "
            "delivery threshold, a page size, a timeout, a promotion window — "
            "somebody else's calendar, and those are the candidates. The order of "
            "the steps in a workflow, the way a total is put together, the algorithm "
            "itself — engineering, and those should stay behind the pipeline where "
            "it is properly difficult to change them. [[slnc 400]] And then the "
            "second question, which is the one that gets skipped: what can I break "
            "by typing into that box? [[slnc 300]] If the answer is anything like "
            "the whole shop, then the guards are not optional extras you will get "
            "round to next quarter. They are the price of admission. [[slnc 350]] "
            "One more distinction, because these two get muddled constantly. This is "
            "not the same thing as a feature flag. Externalised configuration holds "
            "parameters, and a parameter lives for as long as the product does — "
            "there will always be some free-delivery threshold. A feature flag holds "
            "a switch that picks between two code paths, and a switch is supposed to "
            "die: once the new path is proven, you delete the flag and you delete the "
            "old path. [[slnc 350]] Flags that are never removed turn a codebase into "
            "a maze of paths nobody dares delete. That is the failure mode of that "
            "pattern. The failure mode of this one is the quiet minus one."
        ),
    ),
    dict(
        key="17-outro",
        kind="outro",
        title="Thanks for Watching",
        body=[
            "Full source, notes, diagrams and an animated walkthrough",
            "are in the repository — including the exercise that widens",
            "the allowed range and shows the shop giving delivery away",
            "with validation switched on, because the type was never",
            "the guard. The range is.",
        ],
        narration=(
            "That's externalised configuration. [[slnc 250]] If you take one "
            "sentence away, take this one: take the number out of the code, and you "
            "take the compiler, the reviewer and the history out with it. [[slnc "
            "350]] The full source, the written notes, the diagrams and an animated "
            "walkthrough are all in the repository, and everything runs offline with "
            "nothing installed but a Java development kit — no configuration server, "
            "no Spring, no Docker. There is also an optional version that wires it "
            "up to a real config server over HTTP, if you want to see it for "
            "yourself. [[slnc 300]] If you try one exercise, try this one. Widen the "
            "declared range so that the lowest allowed value is minus a thousand "
            "pounds, and then run the demo again. [[slnc 250]] Minus one is now "
            "accepted, and the shop gives delivery away on every order with "
            "validation fully switched on. [[slnc 300]] That is the point worth "
            "sitting with. The type was never the guard. The range is — and the range "
            "is a conversation with somebody who is not an engineer, which is "
            "probably why it is the part that gets left out. [[slnc 300]] If this "
            "helped, a like genuinely does help other people find it, and subscribe "
            "if you would like the rest of the series. [[slnc 250]] Thanks for "
            "watching, and I'll see you in the next one."
        ),
    ),
]
