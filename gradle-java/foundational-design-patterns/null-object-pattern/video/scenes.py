"""Scene definitions for the Null Object teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Null Object',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Null Object pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] Instead of returning '
            'nothing, return an object that does nothing. [[slnc 300]] It '
            'implements the same interface as the real objects. [[slnc '
            '300]] So callers never have to check whether they got '
            'anything. [[slnc 600]] Think of a blank voucher that is '
            'worth nothing. [[slnc 300]] The till can accept it like any '
            'other voucher. [[slnc 300]] It simply takes nothing off the '
            'price. [[slnc 700]] In our online store, the thing that '
            'might not be there is a discount. [[slnc 500]] In this '
            'video, null checks spread, and one gets forgotten. [[slnc '
            '300]] Then this pattern removes them. [[slnc 300]] And we '
            'will hear the part most explanations leave out: how it can '
            'hide a real error. [[slnc 300]] And when not to use it.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Most customers have no discount.', 'Some have a loyalty discount.', 'A few have a staff discount.', '', 'Eight places in the checkout price', 'an order after the discount.'],
        narration=(
            'Here is the scenario. [[slnc 400]] In our online store, most '
            'customers have no discount. [[slnc 300]] Some have a loyalty '
            'discount. [[slnc 300]] And a few have a staff discount. '
            '[[slnc 500]] Eight different places in the checkout work out '
            "an order's price, after any discount. [[slnc 500]] So here "
            'is the question. [[slnc 300]] What should the discount '
            'lookup return, for a customer who has none?'
        ),
    ),
    dict(
        key='03-null', kind='console', title='Return Null',
        body="""ONE. find() returns null.
  customer 1, loyalty:
  total 9000
  customer 2, none:
  total 10000

  the eighth place, taxBase,
  for customer 2:
  NullPointerException.""",
        narration=(
            'The obvious answer is null, meaning nothing. [[slnc 400]] '
            'And it works, as long as everyone remembers to check. [[slnc '
            '500]] Customer one has a loyalty discount, and pays ninety '
            'pounds. [[slnc 300]] Customer two has none, and pays one '
            'hundred pounds. [[slnc 500]] But eight places work out the '
            'price. [[slnc 300]] Seven remembered to check for null. '
            '[[slnc 300]] The eighth, added last, in a hurry, did not. '
            '[[slnc 500]] For customer two, it crashes with a null '
            'pointer exception. [[slnc 300]] At checkout, in front of a '
            'customer.'
        ),
    ),
    dict(
        key='04-blind', kind='console', title='The Check You Stop Seeing',
        body="""TWO. The check.
  if (discount != null)
  appears 7 times.

  the eighth method is the
  one without it.

  seven identical blocks: a
  reader stops seeing them.""",
        narration=(
            'There is another cost, beyond the crash. [[slnc 400]] The '
            'same check, if the discount is not null, appears seven '
            'times. [[slnc 500]] Seven identical blocks. [[slnc 300]] '
            'After the third one, a reader stops noticing them. [[slnc '
            '500]] So the eighth method, the one without the check, hides '
            'in plain sight. [[slnc 300]] It looks just like the others, '
            'minus four lines nobody notices are missing.'
        ),
    ),
    dict(
        key='05-pattern', kind='bullets', title='The Pattern',
        body=['A NoDiscount that implements the same', 'Discount interface.', '', 'apply(price) returns the price', 'unchanged.', '', 'find() never returns null.'],
        narration=(
            'Now, the pattern: a No Discount object. [[slnc 400]] It '
            'implements the same Discount interface as the loyalty and '
            'staff discounts. [[slnc 300]] Its apply method simply '
            'returns the price, unchanged. [[slnc 500]] And the lookup '
            'never returns null. [[slnc 300]] For a customer with no '
            'discount, it returns this object.'
        ),
    ),
    dict(
        key='06-after', kind='console', title='Every Check Deleted',
        body="""THREE. The pattern.
  customer 1: 9000
  customer 2: 10000
  customer 3: 7500
  customer 4: 10000
  all same as before.

  taxBase for customer 2:
  10000, not an exception.""",
        narration=(
            'Third demo: every null check deleted. [[slnc 400]] All eight '
            'methods lose their null checks. [[slnc 300]] Then the same '
            'four customers run again. [[slnc 500]] Ninety pounds. [[slnc '
            '200]] One hundred pounds. [[slnc 200]] Seventy-five pounds. '
            '[[slnc 200]] One hundred pounds. [[slnc 300]] Exactly the '
            'same as before. [[slnc 500]] And the eighth method, which '
            'crashed, now returns one hundred pounds. [[slnc 300]] The '
            'forgotten check can no longer be forgotten, because there is '
            'nothing to remember.'
        ),
    ),
    dict(
        key='07-hides', kind='console', title='The Bill: It Hides Errors',
        body="""FOUR. The bill.
  the service is down.

  a directory that turns any
  failure into no discount:

  customer 1, entitled to
  loyalty, charged 10000
  instead of 9000.

  no error, no log, no alert.""",
        narration=(
            'Now the cost, the part most explanations leave out. [[slnc '
            '300]] A null object can hide errors. [[slnc 500]] Suppose '
            'the discount service is down. [[slnc 300]] A well-meaning '
            'lookup catches the failure, and returns No Discount, to keep '
            'checkout running. [[slnc 500]] Customer one is entitled to '
            'ten percent off. [[slnc 300]] But is charged one hundred '
            'pounds, instead of ninety. [[slnc 300]] No error. [[slnc '
            '200]] No log. [[slnc 200]] No alert. [[slnc 500]] Having no '
            'discount, and the service being down, now look exactly the '
            'same. [[slnc 300]] That is a quieter bug than the crash it '
            'replaced, and a worse one.'
        ),
    ),
    dict(
        key='08-line', kind='bullets', title='Where The Line Is',
        body=['Legitimate domain state:', 'no discount is normal.', 'A null object is right.', '', 'Something went wrong:', 'the service is down.', 'A null object is wrong.'],
        narration=(
            'So where is the line? [[slnc 400]] If absence is a normal '
            'state in your business, a null object is right. [[slnc 300]] '
            'Having no discount is normal. [[slnc 300]] Most customers '
            'have none. [[slnc 500]] But if absence means something went '
            'wrong, like the service being down, a null object is wrong. '
            '[[slnc 300]] It turns a failure into a normal-looking '
            'result.'
        ),
    ),
    dict(
        key='09-optional', kind='console', title='The Honest Alternatives',
        body="""FIVE. Alternatives.
  Optional: customer 1: true,
  customer 2: false.
  absence is in the type.

  service down: still an
  exception, not an empty
  Optional.

  or throw explicitly.""",
        narration=(
            'Fourth demo: the honest alternatives. [[slnc 400]] First, '
            "Java's Optional type. [[slnc 300]] Absence is written into "
            'the return type itself. [[slnc 300]] Customer one has a '
            'discount, and customer two has an empty optional. [[slnc '
            '500]] And a service that is down still throws an error. '
            '[[slnc 300]] It never becomes an empty optional. [[slnc '
            '300]] So the two cases can no longer be confused. [[slnc '
            '300]] And every caller must decide what absence means. '
            '[[slnc 500]] The second alternative: when absence means '
            'something went wrong, throw an error, clearly.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['Collections.emptyList()', 'InputStream.nullInputStream()', 'A no-op logger', 'A class called Noop... or Null...', 'with empty method bodies.'],
        narration=(
            'How can you spot this pattern in code someone else wrote? '
            "[[slnc 400]] Java's empty list is one: a list that is never "
            'null, and holds nothing. [[slnc 300]] The null input stream '
            'reads nothing. [[slnc 300]] A logger that does nothing, '
            'handed to code that would otherwise check whether logging is '
            'set up. [[slnc 300]] And any class named no-op, or null '
            'something, with empty method bodies.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use it when absence is a legitimate', 'domain state.', '', 'Never use it to hide a failure.', '', 'Prefer Optional where the caller', 'must decide.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Use a null object when '
            'absence is a normal state in your business. [[slnc 300]] '
            'Never use one to hide a failure. [[slnc 500]] And where the '
            'caller should decide what absence means, prefer Optional.'
        ),
    ),
    dict(
        key='12-toydb', kind='bullets', title='What Is Real Here',
        body=['Everything is plain Java.', 'The discount service is simulated', 'by a switch that makes it fail.', '', 'The crash and the silent full-price', 'order both really happen.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 400]] '
            'Everything is plain Java. [[slnc 300]] The discount service '
            'is simulated by a switch that makes it fail. [[slnc 500]] '
            'But the crash, and the silent full-price order, both really '
            'happen, in the code you just heard about.'
        ),
    ),
    dict(
        key='13-too-much', kind='bullets', title='When This Is Too Much',
        body=['For a value with one call site,', 'a null check is simpler.', '', 'It earns its place when the same', 'check would be repeated, and when', 'absence is normal.'],
        narration=(
            'So, when is this too much? [[slnc 400]] For a value used in '
            'only one place, a single null check is simpler. [[slnc 400]] '
            'A null object earns its place when the same check would be '
            'repeated. [[slnc 300]] And when absence is normal.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Write a test that would catch', 'a directory swallowing an outage.'],
        narration=(
            "That's the Null Object pattern. [[slnc 400]] If you remember "
            'one sentence, make it this one. [[slnc 300]] Absence can be '
            'a normal state, but it must never be a place to hide a '
            'failure. [[slnc 500]] The full source code, written notes, '
            'diagrams, and an animated walkthrough are all in the '
            'repository. [[slnc 500]] Here is one exercise to try. [[slnc '
            '300]] Write a test that would catch a lookup quietly hiding '
            'a service outage. [[slnc 500]] If this helped, a like really '
            'does help other people find it. [[slnc 300]] And subscribe, '
            "if you'd like the rest of the series. [[slnc 400]] Thanks "
            'for watching.'
        ),
    ),
]
