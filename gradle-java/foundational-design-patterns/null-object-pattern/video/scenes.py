"""Scene definitions for the Null Object teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Null Object',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Null Object '
            'pattern in Java, and it is written and presented by '
            'Jayasekhar Konduru. [[slnc 300]] The plain definition: '
            'instead of returning nothing, return an object that '
            'implements the same interface and does nothing, so callers '
            'never have to check. [[slnc 350]] This is the first project '
            'in the foundational category, whose subject is how an object '
            'gets hold of another, and what happens when there is not '
            'one. Null Object answers the second half. In our online '
            'store, the thing that might not be there is a discount. '
            '[[slnc 300]] By the end you will see how null checks spread '
            'and one gets forgotten, how this pattern removes them, and, '
            'the part most treatments leave out, how it can hide an '
            'error. I will also tell you plainly when I would not use it.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Most customers have no discount.', 'Some have a loyalty discount.', 'A few have a staff discount.', '', 'Eight places in the checkout price', 'an order after the discount.'],
        narration=(
            'Here is the scenario. In the online store, most customers '
            'have no discount. Some have a loyalty discount, and a few, a '
            'staff discount. [[slnc 300]] Eight different places in the '
            'checkout price an order after whatever discount there is. '
            '[[slnc 300]] The question: what should the lookup return, '
            'for a customer who has none?'
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
            'The obvious answer is null. And it works, when everyone '
            'remembers to check. Customer one, with a loyalty discount: '
            'ninety pounds. Customer two, with none: one hundred pounds. '
            '[[slnc 300]] But there are eight places that price an order. '
            'Seven remembered to check for null. The eighth, added last, '
            'in a hurry, did not. [[slnc 300]] For customer two, it '
            'throws a null pointer exception, at checkout, in front of a '
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
            'Look at the cost, beyond the crash. The same check, if '
            'discount is not null, appears seven times. [[slnc 300]] '
            'Seven identical blocks. After the third, a reader stops '
            'seeing them. So the eighth method, the one without the '
            'check, hides in plain sight. It looks exactly like all the '
            'others, minus four lines nobody notices are missing.'
        ),
    ),
    dict(
        key='05-pattern', kind='bullets', title='The Pattern',
        body=['A NoDiscount that implements the same', 'Discount interface.', '', 'apply(price) returns the price', 'unchanged.', '', 'find() never returns null.'],
        narration=(
            'The pattern: a no discount object. It implements the same '
            'discount interface as the loyalty and staff discounts. Its '
            'apply method just returns the price unchanged. [[slnc 300]] '
            'The lookup never returns null. For a customer with no '
            'discount, it returns this.'
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
            'Now delete every null check, in all eight methods. Run the '
            'same four customers. Nine thousand. Ten thousand. '
            'Seventy-five hundred. Ten thousand. Identical to before, '
            'every one. [[slnc 300]] And the eighth method, that crashed, '
            'now returns ten thousand. The forgotten check is no longer '
            'possible to forget, because there is nothing to remember.'
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
            'Now the bill, the part most explanations leave out. A null '
            'object hides errors. [[slnc 300]] Suppose the discount '
            'service is down. A well-meaning directory catches the '
            'failure, and returns the no discount object, to keep the '
            'checkout going. [[slnc 300]] Customer one, entitled to ten '
            'per cent off, is charged ten thousand pence instead of nine '
            'thousand. No error. No log. No alert. [[slnc 300]] No '
            'discount, and the service was down, now look exactly the '
            'same. That is a quieter bug than the exception it replaced, '
            'and a worse one.'
        ),
    ),
    dict(
        key='08-line', kind='bullets', title='Where The Line Is',
        body=['Legitimate domain state:', 'no discount is normal.', 'A null object is right.', '', 'Something went wrong:', 'the service is down.', 'A null object is wrong.'],
        narration=(
            'So where is the line? If absence is a legitimate state of '
            'the domain, a null object is right. Having no discount is '
            'normal, most customers have none. [[slnc 300]] If absence '
            'means something went wrong, the service is down, a null '
            'object is wrong. It turns a failure into a normal-looking '
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
            'There are two honest alternatives. First, optional. Absence '
            'is written into the return type. No discount is an empty '
            'optional. A service that is down is still an exception. The '
            'two can no longer be confused, and every caller has to '
            'decide what absence means to it. In Java, this is often the '
            'better answer. [[slnc 300]] Second, an explicit failure. '
            'When absence means something went wrong, throw.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['Collections.emptyList()', 'InputStream.nullInputStream()', 'A no-op logger', 'A class called Noop... or Null...', 'with empty method bodies.'],
        narration=(
            'How do you recognise this in code you did not write? '
            'Collections dot empty list is one: a list that is never '
            'null, and does nothing. Input stream null input stream reads '
            'nothing. A no-op logger, handed to code that would otherwise '
            'check whether logging is configured. And any class called '
            'noop or null, implementing an interface with empty method '
            'bodies.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use it when absence is a legitimate', 'domain state.', '', 'Never use it to hide a failure.', '', 'Prefer Optional where the caller', 'must decide.'],
        narration=(
            'Here is my verdict, plainly. Use a null object when absence '
            'is a legitimate state of your domain. Never use one to hide '
            'a failure. And where the caller ought to decide what absence '
            'means, prefer optional.'
        ),
    ),
    dict(
        key='12-toydb', kind='bullets', title='What Is Real Here',
        body=['Everything is plain Java.', 'The discount service is simulated', 'by a switch that makes it fail.', '', 'The crash and the silent full-price', 'order both really happen.'],
        narration=(
            'The same honest admission as everywhere in this course. It '
            'is all plain Java. The discount service is simulated by a '
            'switch that makes it fail. But the crash, and the silent '
            'full price order, both really happen, in the code you have '
            'just seen.'
        ),
    ),
    dict(
        key='13-too-much', kind='bullets', title='When This Is Too Much',
        body=['For a value with one call site,', 'a null check is simpler.', '', 'It earns its place when the same', 'check would be repeated, and when', 'absence is normal.'],
        narration=(
            'So when is it too much? For a value with a single call site, '
            'a null check is simpler. It earns its place when the same '
            'check would be repeated, and when absence is normal.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Write a test that would catch', 'a directory swallowing an outage.'],
        narration=(
            "That's the Null Object. [[slnc 250]] If you take one "
            'sentence away, take this one: absence can be a normal state, '
            'but it must never be a place to hide a failure. [[slnc 350]] '
            'The full source, the written notes, the diagrams and an '
            'animated walkthrough are all in the repository, running '
            'offline with nothing installed but a Java development kit. '
            '[[slnc 300]] If you try one exercise, write a test that '
            'would catch a directory swallowing an outage. [[slnc 300]] '
            'If this helped, a like genuinely does help other people find '
            'it, and subscribe if you would like the rest of the series. '
            '[[slnc 250]] Thanks for watching.'
        ),
    ),
]
