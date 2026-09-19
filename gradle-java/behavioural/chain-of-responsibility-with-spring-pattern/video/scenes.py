"""Scene definitions for the Chain of Responsibility with Spring teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Chain of Responsibility with Spring',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Chain of '
            'Responsibility pattern with Spring Boot, in Java, and it is '
            'written and presented by Jayasekhar Konduru. [[slnc 300]] It '
            'is the framework version of the Chain of Responsibility '
            'video. That one passed a checkout request along address, '
            'stock, fraud and payment checks, stopping at the first that '
            'answered, and reported which links never ran. This one shows '
            'the same idea inside Spring Boot. [[slnc 350]] The plain '
            'definition, in short: in Spring, the links are beans of one '
            'interface, and the container hands you the list, already in '
            'order. [[slnc 300]] By the end you will see the same '
            'screening built from beans, then see what changes: the order '
            'becomes a cost, a failing link needs a policy, and a '
            'property can remove a check.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Chain of Responsibility, the hand-built', 'video, passes a checkout request', 'along four checks and stops at the', 'first that answers.', '', 'If you have not seen it, start there.'],
        narration=(
            'This video assumes the Chain of Responsibility video. If you '
            'have not seen it, start there. It passes a checkout request '
            'along address, stock, fraud and payment checks, stops at the '
            'first that answers, and reports which links never ran. '
            '[[slnc 300]] This one uses the same example. It does not '
            'teach the pattern again. It shows what Spring Boot does with '
            'it.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Line',
        body=['One thing is new: Spring Boot.', '', 'It injects every bean of one', 'interface as an ordered list.', '', 'Skipping this video loses none', 'of the pattern.'],
        narration=(
            'Before the first line of code, what Spring Boot is. Spring '
            'is a framework whose core is a container that creates your '
            'objects. It can inject every bean of one interface as a '
            'list, sorted by an order annotation. [[slnc 300]] And a '
            'promise: skipping this video loses none of the pattern. The '
            'hand-built one teaches all of it.'
        ),
    ),
    dict(
        key='04-build', kind='console', title='Spring Builds The Chain',
        body="""ONE. Builds the chain.
  order:
  address, stock, fraud,
  payment-limit.

  from @Order numbers on four
  different classes.""",
        narration=(
            'First, the chain. Spring injects the four checks in order: '
            'address, stock, fraud, payment limit. Where does that order '
            'come from? From order numbers, written on four different '
            'classes. No single file shows the chain.'
        ),
    ),
    dict(
        key='05-run', kind='console', title='Five Requests',
        body="""TWO. Five requests.
  asha: approved by fallback.
  erin: rejected by address.
  ben: rejected by stock.
  carol: rejected by fraud.
  dev: referred by payment.""",
        narration=(
            'Second, five requests. Asha passes every check, and the '
            'fallback approves her. Erin is rejected by the address '
            'check, and three links never ran. Ben is stopped by stock. '
            'Carol by fraud. Dev is referred by the payment limit.'
        ),
    ),
    dict(
        key='06-cost', kind='console', title='The Order Is The Cost',
        body="""THREE. The order.
  cheap checks first: 3 paid
  calls.

  the paid check first: 5.

  same checks, same answers.""",
        narration=(
            'Third, the order is the cost. With the cheap checks first, '
            'only three of the five requests reach the paid fraud '
            'service. Put the paid check first, and all five do. [[slnc '
            '300]] Same checks, same answers, and a different bill. In '
            'Spring, a single order number changes it.'
        ),
    ),
    dict(
        key='07-throws', kind='console', title='A Link That Throws',
        body="""FOUR. A link throws.
  asha: referred by fraud.
  fraud check failed:
  fraud service unavailable.

  the caller saw no error.""",
        narration=(
            'Fourth, a link that throws. The fraud service is down. The '
            'chain catches the exception and refers the order to a '
            'person. The caller sees a decision, not an error. [[slnc '
            '300]] That is a policy, and it is written in the walker. '
            'Without it, one broken service stops every checkout.'
        ),
    ),
    dict(
        key='08-off', kind='console', title='Switched Off By A Property',
        body="""FIVE. A property.
  order: address, stock,
  payment-limit.

  carol: approved.

  no code changed.""",
        narration=(
            'Fifth, a property. Set one setting to false, and the fraud '
            'link disappears. The chain is three links long. Carol, who '
            'was rejected before, is approved. [[slnc 300]] No code '
            'changed. That is convenient in a test, and dangerous in '
            'production, so print the order at startup.'
        ),
    ),
    dict(
        key='09-fallback', kind='console', title='Nobody Answers',
        body="""SIX. Nobody answers.
  fallback approved: asha
  goes through.
  fallback referred: asha
  is sent to a person.

  a named setting.""",
        narration=(
            'Last, nobody answers. When every link has no opinion, a '
            'fallback answers. It is a named setting. Approved by '
            'default, and referred if you change it. Falling off the end '
            'of a chain should be a decision, not an accident.'
        ),
    ),
    dict(
        key='10-verdict', kind='bullets', title='The Verdict',
        body=['Cheap and decisive links first.', '', 'Decide what a throwing link means.', '', 'Print the order at startup.', '', 'Test the whole chain.'],
        narration=(
            'My verdict, plainly. Put cheap and decisive links first. '
            'Decide what a throwing link means. Print the order at '
            'startup. And test the whole chain.'
        ),
    ),
    dict(
        key='11-recognise', kind='bullets', title='How To Recognise It',
        body=['A List of an interface in a', 'constructor, with Order on the', 'implementations.', '', 'A loop that stops at the first answer.'],
        narration=(
            'How do you recognise this in code you did not write? A list '
            'of an interface in a constructor, with order annotations on '
            'the implementations. And a loop that stops at the first '
            'answer.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=["Servlet filters, Spring Security's", 'filter chain and validation', 'pipelines.'],
        narration=(
            "You have met this in servlet filters, Spring Security's "
            'filter chain, and validation pipelines.'
        ),
    ),
    dict(
        key='13-versions', kind='bullets', title='What Was Used',
        body=['Spring Boot 4.1.1.', '', 'No web server, no database,', 'no web starter.'],
        narration=(
            'For the record. Spring Boot four point one point one. No web '
            'server, no database, and no web starter.'
        ),
    ),
    dict(
        key='14-real', kind='bullets', title='What Is Real Here',
        body=["Everything is real: Spring's", 'container and its ordering.', '', 'The paid service is counted, not', 'really paid.'],
        narration=(
            'The same honest admission as everywhere in this course. '
            "Everything is real: Spring's container and its ordering. The "
            'paid fraud service is a counter, not a real service.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['For two checks that never change,', 'an if statement is clearer.'],
        narration=(
            'So when is it too much? For two checks that never change, an '
            'if statement is clearer than a chain.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Give two checks the same order', 'number and see what happens.'],
        narration=(
            "That's Chain of Responsibility with Spring. [[slnc 250]] If "
            'you take one sentence away, take this one: Spring builds and '
            'orders the chain, and the order becomes a cost you have to '
            'watch. [[slnc 350]] The full source, the written notes, the '
            'diagrams and an animated walkthrough are all in the '
            'repository. [[slnc 300]] If you try one exercise, give two '
            'checks the same order number, and see what happens. [[slnc '
            '300]] If this helped, a like genuinely does help other '
            'people find it, and subscribe if you would like the rest of '
            'the series. [[slnc 250]] Thanks for watching.'
        ),
    ),
]
