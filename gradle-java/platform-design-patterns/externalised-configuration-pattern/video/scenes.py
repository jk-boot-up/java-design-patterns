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
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Externalised Configuration pattern, in Java. [[slnc 300]] '
            'This video is presented by Jayasekhar Konduru. [[slnc 600]] '
            'First, a simple definition. [[slnc 300]] Externalised '
            'configuration keeps the values your program needs outside '
            'the program itself. [[slnc 300]] And the program reads them '
            'while it runs. [[slnc 300]] So changing one of those values '
            'does not mean building and releasing a new program. [[slnc '
            '600]] Think of a greengrocer with a chalk board outside the '
            'shop. [[slnc 300]] The prices are not painted on the wall. '
            '[[slnc 300]] To change a price, someone rubs it out and '
            'chalks a new one, in thirty seconds. [[slnc 300]] But '
            'because the board is outside, anyone can also write nonsense '
            'on it. [[slnc 700]] In our online store, delivery is free '
            'for anyone spending over fifty pounds. [[slnc 300]] And the '
            'marketing team want that to be thirty-five pounds by '
            'Saturday morning. [[slnc 500]] By the end, you will know why '
            'a well-written constant can still be in the wrong place. '
            '[[slnc 300]] Exactly where the value must be read. [[slnc '
            '300]] And the four safety checks a value loses when it '
            'leaves your code, and how to get them back.'
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
            "Here is the scenario. [[slnc 400]] The shop's delivery page "
            'makes one promise. [[slnc 300]] Spend over fifty pounds, and '
            'delivery is free. [[slnc 300]] Spend less, and delivery '
            'costs four pounds ninety-nine. [[slnc 600]] Three baskets '
            'are waiting at the checkout. [[slnc 300]] Every demo uses '
            'these same three. [[slnc 300]] The first holds sixty-two '
            'pounds of goods. [[slnc 300]] The second, forty-eight '
            'pounds. [[slnc 300]] The third, thirty-one pounds fifty. '
            '[[slnc 500]] With a fifty-pound threshold, the first ships '
            'free, and the other two pay. [[slnc 600]] Then, on Friday '
            'afternoon at half past four, marketing ask for a change. '
            '[[slnc 300]] For the weekend campaign, free delivery over '
            'thirty-five pounds, instead of fifty. [[slnc 300]] A '
            'one-number change. [[slnc 300]] Remember that Friday half '
            'past four.'
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
            'Here is where the fifty pounds lives today. [[slnc 300]] It '
            'is a constant in the checkout class, with a clear name. '
            '[[slnc 600]] And there is nothing wrong with it. [[slnc '
            '300]] It has a name, so it is not a mystery number. [[slnc '
            '300]] It is typed as money, so it cannot be mistaken for '
            'anything else. [[slnc 300]] It appears in one place only. '
            '[[slnc 300]] Any code reviewer would approve it. [[slnc '
            "600]] So let's be clear. [[slnc 300]] This pattern does not "
            'fix bad code. [[slnc 300]] It fixes a value that sits '
            'somewhere that changes too slowly. [[slnc 500]] The code is '
            'fine. [[slnc 300]] The problem is what it takes to turn '
            'fifty into thirty-five.'
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
            'First demo: what changing one number costs. [[slnc 400]] The '
            'change goes through a normal release process. [[slnc 600]] '
            'Editing the constant takes fifteen minutes, and is done at a '
            'quarter to five on Friday. [[slnc 300]] Then code review, '
            'forty-five minutes. [[slnc 300]] But it finishes on Monday '
            'morning. [[slnc 300]] Because the release window closed at '
            'five on Friday, and only reopens on Monday. [[slnc 600]] '
            'Then building and testing: twenty-five minutes. [[slnc 300]] '
            'Release approval: half an hour. [[slnc 300]] Then the '
            'release itself, and twenty minutes watching it. [[slnc 600]] '
            'Two hours and fifteen minutes of real work. [[slnc 300]] And '
            'it goes live on Monday at a quarter to eleven. [[slnc 300]] '
            'Two days after the Saturday promotion started. [[slnc 300]] '
            'All weekend, the campaign promises free delivery over '
            'thirty-five pounds, and the shop charges as if it were '
            'fifty. [[slnc 600]] Now try to remove a step. [[slnc 300]] '
            'Code review stops typos reaching customers. [[slnc 300]] '
            'Tests stop broken code being released. [[slnc 300]] Approval '
            'proves releases are controlled. [[slnc 300]] And weekday '
            'windows exist because the people who would spot a bad '
            'release are at work on weekdays. [[slnc 500]] Nothing on '
            'that list is waste. [[slnc 300]] And the promotion still '
            'misses its weekend. [[slnc 300]] That is not a code quality '
            'problem.'
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
            'So here is the idea, and it starts with a distinction. '
            '[[slnc 500]] Some values in your program are decisions about '
            'behaviour. [[slnc 300]] The order of steps, how a total is '
            'built, the method you chose. [[slnc 300]] Those belong '
            'behind the release process. [[slnc 300]] And you should be '
            'glad they are hard to change. [[slnc 600]] Other values are '
            'business policy. [[slnc 300]] A threshold, a page size, a '
            'promotion window, how long a session lasts. [[slnc 300]] '
            "These change on someone else's timetable, usually not an "
            "engineer's. [[slnc 600]] Here is the key sentence. [[slnc "
            '300]] Putting a policy value behind the release process does '
            'not make it safer. [[slnc 300]] It makes it late. [[slnc '
            '600]] So externalised configuration keeps that kind of value '
            'outside the program. [[slnc 300]] And reads it while the '
            'program runs. [[slnc 300]] That is the whole pattern.'
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
            'It takes three moves. [[slnc 300]] Most explanations only '
            'give you two. [[slnc 600]] Move one. [[slnc 200]] The value '
            'comes from outside. [[slnc 300]] And it is read every single '
            'time it is used. [[slnc 300]] Not once, when the program '
            'starts. [[slnc 300]] Every time. [[slnc 600]] Move two. '
            '[[slnc 200]] The code still carries its own default value. '
            '[[slnc 300]] Because the outside source might be '
            'unreachable. [[slnc 300]] And a shop that stops selling '
            'because a settings server is down is worse than one with the '
            'number built in. [[slnc 600]] Move three, the one usually '
            'skipped. [[slnc 300]] While the value lived in the code, '
            'four things protected it. [[slnc 300]] The compiler, which '
            'refuses to build if you type the word fifty where a number '
            'belongs. [[slnc 300]] The type system, which keeps it as '
            'money. [[slnc 300]] A code reviewer, who would question '
            'minus one pound. [[slnc 300]] And version control, which '
            'records who changed it, when, and what it was before. [[slnc '
            '600]] None of those four follows the value out of the code. '
            '[[slnc 300]] If you want them, you must rebuild them '
            'yourself.'
        ),
    ),
    dict(
        key="07-roles",
        kind="diagram",
        title="Who Does What",
        body=None,
        narration=(
            "Let's name the pieces. [[slnc 300]] There are five. [[slnc "
            '600]] First, the checkout. [[slnc 300]] It works out whether '
            'a basket gets free delivery. [[slnc 300]] That arithmetic is '
            'the same in both versions of this project. [[slnc 500]] '
            'Second, the settings reader. [[slnc 300]] It is the only '
            'part that knows about the outside world. [[slnc 300]] '
            'Checkout asks it for the threshold, and gets back an amount. '
            '[[slnc 300]] Checkout cannot tell whether it came from a '
            'server, a file, or the built-in default. [[slnc 500]] Third, '
            'the declared setting. [[slnc 300]] A small record holding '
            "four things. [[slnc 300]] The setting's name, its default, "
            'the lowest sensible value, and the highest. [[slnc 300]] '
            'This will replace the compiler. [[slnc 500]] Fourth, the '
            'configuration source. [[slnc 300]] It just stores text under '
            'names. [[slnc 300]] It has no idea whether the text makes '
            'sense. [[slnc 500]] Fifth, a change log. [[slnc 300]] It '
            'records every change: the setting, the new value, the old '
            'value, who, and when. [[slnc 300]] That replaces version '
            'control. [[slnc 600]] The project has two checkouts, one '
            'with the number in the code, and one that reads it. [[slnc '
            '300]] And two settings readers, one that trusts any text, '
            'and one that checks it. [[slnc 300]] The same bad values go '
            'through both.'
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
            'Here is the configured checkout, and very little of it is '
            'new. [[slnc 500]] It receives a basket. [[slnc 300]] It asks '
            'the settings reader for the free-delivery threshold. [[slnc '
            '300]] If the basket is worth at least that much, delivery is '
            'free. [[slnc 300]] Otherwise, it charges the standard fee. '
            '[[slnc 500]] Only one line differs from the hard-coded '
            'version. [[slnc 300]] Instead of using a constant, it asks '
            'for a setting. [[slnc 600]] Now the most important detail in '
            'this video. [[slnc 300]] Not what that line says, but where '
            'it sits. [[slnc 500]] It sits inside the method that prices '
            'each basket. [[slnc 300]] So every time a customer reaches '
            'delivery, the threshold is fetched again. [[slnc 600]] '
            'Tidy-minded developers want to move it to the start, and '
            'keep the value. [[slnc 300]] It looks neater. [[slnc 300]] '
            'And it breaks the pattern. [[slnc 300]] Because now the only '
            'way to pick up a new value is to restart the program. [[slnc '
            '300]] One test exists only to fail if someone makes that '
            'tidy-up. [[slnc 600]] And one more thing. [[slnc 300]] What '
            'comes back is the amount, plus a note of where it came from. '
            '[[slnc 300]] Once a value can change, the question becomes: '
            'which threshold applied to this order, and where did it come '
            'from?'
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
            'Second demo: what it buys. [[slnc 400]] It starts with '
            'nothing configured. [[slnc 300]] So every quote uses the '
            'built-in default, and the shop behaves exactly as before. '
            '[[slnc 300]] The sixty-two-pound basket ships free, and the '
            'other two pay. [[slnc 300]] Adopting the pattern changed '
            'nothing on its own. [[slnc 600]] Then someone in marketing '
            'types thirty-five into a box. [[slnc 500]] Four seconds '
            'later, the very next basket is priced against thirty-five '
            'pounds. [[slnc 300]] And the forty-eight-pound basket now '
            'ships free. [[slnc 600]] No rebuild. [[slnc 200]] No '
            'release. [[slnc 200]] No restart. [[slnc 300]] Nobody '
            'approved anything. [[slnc 500]] Four seconds, against two '
            'hours of work spread over a whole weekend. [[slnc 300]] That '
            'is the business case for this pattern. [[slnc 600]] That is '
            'the good news. [[slnc 300]] The rest of this video is the '
            'bill.'
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
            'Third demo: the source goes away. [[slnc 400]] The '
            'connection to the settings server drops. [[slnc 300]] Every '
            'setting falls back to its built-in default. [[slnc 300]] And '
            'the shop keeps selling. [[slnc 300]] That is exactly why '
            'move two insisted on a default. [[slnc 600]] But listen to '
            'what it quietly lost. [[slnc 300]] The threshold is back to '
            'fifty pounds. [[slnc 300]] The promotion is off. [[slnc '
            '300]] The campaign is still promising thirty-five pounds, '
            'and the shop is charging as if it were fifty. [[slnc 600]] '
            'And nothing reports it. [[slnc 300]] No error, no log, no '
            'alert. [[slnc 300]] The only trace is that little note '
            'saying where the value came from. [[slnc 500]] Surviving an '
            'outage quietly is not the same as surviving it correctly.'
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
            'Fourth demo: a number nobody checked. [[slnc 400]] Saturday '
            'morning, twelve minutes past nine. [[slnc 300]] Someone '
            'types minus one into the box. [[slnc 300]] Perhaps they hit '
            'the wrong key. [[slnc 600]] The settings server stores it, '
            'because storing text is all it does. [[slnc 300]] Now every '
            'basket is worth more than minus one pound. [[slnc 300]] So '
            'every basket ships free. [[slnc 300]] Including the '
            'thirty-one-pound basket, where delivery costs more than the '
            'shop earns. [[slnc 600]] And nothing goes wrong, as far as '
            'the software can tell. [[slnc 300]] No error, no crash, no '
            'alert. [[slnc 300]] Minus one is a perfectly valid number. '
            '[[slnc 300]] The program was told the threshold is minus one '
            'pound, and it obeys. [[slnc 600]] The first sign is the '
            'profit report, on Monday. [[slnc 300]] That value reached '
            'the live shop in four seconds. [[slnc 300]] With no '
            'compiler, no review, and no tests in the way. [[slnc 300]] '
            'That is what you traded the release process for.'
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
            'Fifth demo: not a number at all. [[slnc 400]] Eight minutes '
            'later, someone tries to fix it. [[slnc 300]] And types the '
            'word fifty, in letters. [[slnc 600]] That cannot be turned '
            'into money. [[slnc 300]] So an error is thrown, and nothing '
            'catches it. [[slnc 500]] Not one basket can be priced. '
            '[[slnc 300]] Every customer at the delivery step gets an '
            'error page. [[slnc 300]] The shop is down. [[slnc 300]] '
            'Taken down by someone typing a word into a box, with no code '
            'changed at all. [[slnc 600]] The compiler would have refused '
            'this. [[slnc 300]] But the compiler is no longer between a '
            "person's fingers and your live shop. [[slnc 600]] And here "
            'is an uncomfortable comparison. [[slnc 300]] Of these two '
            'failures, this one is better. [[slnc 300]] Because you find '
            'out. [[slnc 300]] Errors spike, someone is called, and it is '
            'fixed within minutes. [[slnc 300]] Minus one runs all '
            'weekend, quietly, and the first to notice is an accountant. '
            '[[slnc 500]] A loud failure is a bad afternoon. [[slnc 300]] '
            'A quiet failure is a bad quarter.'
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
            "So let's rebuild the four protections, one by one. [[slnc "
            '300]] None of them is difficult. [[slnc 600]] The compiler '
            'refused the word fifty. [[slnc 300]] Its replacement is a '
            'typed setting. [[slnc 300]] It tries to turn the text into '
            'money, and rejects it at the door if it cannot. [[slnc 500]] '
            'A reviewer would have questioned minus one pound. [[slnc '
            '300]] Its replacement is a declared range: a lowest and a '
            'highest allowed value. [[slnc 500]] Version control knew who '
            'changed what, and when. [[slnc 300]] Its replacement is an '
            'audit trail, recording that on every change. [[slnc 500]] '
            'And a bad release was undone by a new release. [[slnc 300]] '
            'Its replacement is a rollback that is as fast as the change '
            'was. [[slnc 600]] Notice what this list is not. [[slnc 300]] '
            'Not a framework, and not clever. [[slnc 300]] Four small, '
            'ordinary pieces of code. [[slnc 300]] This pattern goes '
            'wrong in real systems because the first two moves work on '
            'their own. [[slnc 300]] So nobody gets round to the third.'
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
            'Sixth demo: declared, and checked at the door. [[slnc 400]] '
            'The setting is now declared, out loud. [[slnc 300]] It holds '
            'money. [[slnc 300]] It must be between five pounds and two '
            'hundred pounds. [[slnc 300]] And it defaults to fifty '
            'pounds. [[slnc 600]] Why those limits? [[slnc 300]] Below '
            'five pounds, you are giving free delivery on a packet of '
            'crisps. [[slnc 300]] Above two hundred, almost nobody '
            'qualifies, and the promotion is broken the other way. [[slnc '
            '300]] Those are business judgements. [[slnc 300]] And that '
            'is why the program must enforce them. [[slnc 600]] Now the '
            'word fifty is still in the settings. [[slnc 300]] It is '
            'refused at the door. [[slnc 300]] The shop falls back to '
            'fifty pounds, and keeps trading. [[slnc 500]] Then a good '
            'value, thirty-five, arrives, and passes. [[slnc 300]] And '
            'the reader remembers it as the last known good value. [[slnc '
            '500]] Then someone types minus one again. [[slnc 300]] It is '
            'refused. [[slnc 300]] And the shop falls back, not to fifty, '
            'but to thirty-five, the last good value. [[slnc 600]] That '
            'matters. [[slnc 300]] Someone deliberately set thirty-five '
            'an hour ago. [[slnc 300]] Reverting to fifty because of an '
            'unrelated typo would cancel a promotion nobody decided to '
            'cancel. [[slnc 500]] And both refusals are recorded, loudly. '
            '[[slnc 300]] A guard that silently swallows bad input is '
            'only half a guard.'
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
            'Seventh demo: the trail, and a rollback. [[slnc 400]] Here '
            'is every change made to that one setting. [[slnc 300]] Five '
            'changes, in less than a day. [[slnc 300]] Each records the '
            'new value, the old value, who made it, and exactly when. '
            '[[slnc 600]] Five changes to a business-critical number in '
            'one day. [[slnc 300]] And none of them is in version '
            'control. [[slnc 300]] This list is its replacement. [[slnc '
            '600]] The question you will really be asked is not: what is '
            'the threshold now? [[slnc 300]] You can just look. [[slnc '
            "300]] It is: what was it at nine o'clock on Saturday "
            'morning? [[slnc 300]] Without this list, there is no honest '
            'answer. [[slnc 600]] Then the fourth protection. [[slnc '
            '300]] Saturday, twenty to twelve. [[slnc 300]] Someone on '
            'call sees the threshold is minus one, and rolls it back. '
            '[[slnc 300]] Four seconds later, the shop is using '
            'thirty-five pounds again. [[slnc 500]] Nobody had to '
            'remember the old value. [[slnc 300]] The log had it. [[slnc '
            '500]] The same fix through the release process would have '
            'gone live on Monday. [[slnc 600]] A bad release takes a '
            'release to undo. [[slnc 300]] A bad value takes four '
            'seconds. [[slnc 500]] So externalised configuration is not a '
            'way to avoid control. [[slnc 300]] It is a way to control a '
            'change in seconds, instead of days.'
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
            'So, what should you move outside the code? [[slnc 300]] Ask '
            'two questions, in this order. [[slnc 600]] First: does this '
            "value change on an engineer's timetable, or someone else's? "
            '[[slnc 300]] A free-delivery threshold, a page size, a '
            "timeout, or a promotion window? [[slnc 300]] Someone else's. "
            '[[slnc 300]] Those are candidates. [[slnc 500]] The order of '
            'steps, how a total is built, the method itself? [[slnc 300]] '
            'Those belong in the code, behind the release process. [[slnc '
            '600]] Second: what could I break by typing into that box? '
            '[[slnc 300]] If the answer is the whole shop, the '
            'protections are not optional. [[slnc 300]] They are the '
            'price of entry. [[slnc 600]] One last distinction. [[slnc '
            '300]] This is not the same as a feature flag. [[slnc 300]] A '
            'setting like a threshold lives as long as the product. '
            '[[slnc 300]] A feature flag switches between two versions of '
            'code. [[slnc 300]] And a flag is meant to be deleted, once '
            'the new version is proven.'
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
            "That's the Externalised Configuration pattern. [[slnc 400]] "
            'If you remember one sentence, make it this one. [[slnc 300]] '
            'Take a number out of the code, and you also take out the '
            'compiler, the reviewer, and the history, so rebuild them on '
            'the outside. [[slnc 500]] The full source code, written '
            'notes, diagrams, and an animated walkthrough are all in the '
            'repository. [[slnc 300]] It runs offline, with nothing '
            'installed except a Java development kit. [[slnc 500]] Here '
            'is one exercise to try. [[slnc 300]] Widen the allowed '
            'range, so the lowest value is minus a thousand pounds. '
            '[[slnc 300]] Run the demo again. [[slnc 300]] Now minus one '
            'is accepted, and delivery is given away, even with checking '
            'switched on. [[slnc 300]] The type was never the protection. '
            '[[slnc 300]] The range is. [[slnc 500]] If this helped, a '
            'like really does help other people find it. [[slnc 300]] And '
            "subscribe, if you'd like the rest of the series. [[slnc "
            '400]] Thanks for watching.'
        ),
    ),
]
