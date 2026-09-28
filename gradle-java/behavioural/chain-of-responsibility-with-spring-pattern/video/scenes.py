"""Scene definitions for the Chain of Responsibility with Spring teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Chain of Responsibility with Spring',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Chain of Responsibility pattern, in Java, using Spring Boot. '
            '[[slnc 300]] This video is presented by Jayasekhar Konduru. '
            '[[slnc 600]] First, a simple definition. [[slnc 300]] A '
            'chain passes a request along a line of objects, until one of '
            'them is willing to answer. [[slnc 500]] In Spring, each link '
            'in the chain is a bean of one shared interface. [[slnc 300]] '
            'And Spring hands you the whole list of links, already '
            'sorted. [[slnc 600]] Think of airport security. [[slnc 300]] '
            'Your bag goes through one check after another: passport, '
            'scanner, and a hand search. [[slnc 300]] Any one of them can '
            'stop you. [[slnc 700]] This is the framework version of the '
            'Chain of Responsibility video, with the same online '
            'checkout. [[slnc 400]] We will build the same order checks '
            'from Spring beans. [[slnc 300]] Then we will see what '
            'changes. [[slnc 300]] The order of the checks becomes a '
            'cost, a failing check needs a policy, and a setting can '
            'remove a check.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Chain of Responsibility, the hand-built', 'video, passes a checkout request', 'along four checks and stops at the', 'first that answers.', '', 'If you have not seen it, start there.'],
        narration=(
            'Before we start, a quick note. [[slnc 300]] This video has a '
            'partner: the hand-built Chain of Responsibility video. '
            '[[slnc 400]] That one passes a checkout request along four '
            'checks: address, stock, fraud, and payment. [[slnc 300]] It '
            'stops at the first check that answers, and reports which '
            'checks never ran. [[slnc 500]] If you are new to the '
            'pattern, watch that one first. [[slnc 400]] Here, we keep '
            'the same example, and ask what Spring Boot does with it.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Line',
        body=['One thing is new: Spring Boot.', '', 'It injects every bean of one', 'interface as an ordered list.', '', 'Skipping this video loses none', 'of the pattern.'],
        narration=(
            'One thing is new in this project: Spring Boot. [[slnc 400]] '
            'At its heart, Spring is a container that creates your '
            'objects for you. [[slnc 300]] It can collect every bean of '
            'one interface into a list. [[slnc 300]] And it sorts that '
            'list using an order number written on each class. [[slnc '
            '500]] And one promise. [[slnc 300]] If you skip this video, '
            'you lose none of the pattern. [[slnc 300]] This one is about '
            'the tool.'
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
            'First demo: Spring builds the chain. [[slnc 400]] Spring '
            'hands us the four checks, in this order. [[slnc 300]] '
            'Address, stock, fraud, and payment limit. [[slnc 500]] Where '
            'does that order come from? [[slnc 300]] From order numbers, '
            'written on four different classes. [[slnc 400]] So no single '
            'file shows you the whole chain.'
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
            'Second demo: five customers place orders. [[slnc 400]] Asha '
            'passes every check, so nobody objects, and the fallback '
            'approves her order. [[slnc 400]] Erin is rejected by the '
            'address check. [[slnc 300]] The other three checks never '
            'ran. [[slnc 400]] Ben is stopped by the stock check. [[slnc '
            '300]] Carol is stopped by the fraud check. [[slnc 300]] And '
            'Dev is referred to a person, by the payment limit check.'
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
            'Third demo: the order of the checks is a cost. [[slnc 400]] '
            'The fraud service is paid for, per call. [[slnc 500]] With '
            'the cheap checks first, only three of the five orders reach '
            'the paid fraud service. [[slnc 400]] Put the paid check '
            'first, and all five orders reach it. [[slnc 500]] The same '
            'checks, and the same answers. [[slnc 300]] But a bigger '
            'bill. [[slnc 300]] And in Spring, a single order number '
            'decides it.'
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
            'Fourth demo: a check that crashes. [[slnc 400]] The fraud '
            'service is down, and its check throws an error. [[slnc 500]] '
            "The chain catches the error, and refers Asha's order to a "
            'person. [[slnc 300]] The caller receives a decision, not an '
            'error. [[slnc 500]] That is a policy, and it is written '
            'once, in the code that walks the chain. [[slnc 300]] Without '
            'it, one broken service would stop every checkout.'
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
            'Fifth demo: a setting switches a check off. [[slnc 400]] Set '
            "the fraud check's setting to false, and that check "
            'disappears. [[slnc 300]] The chain is now three checks long. '
            '[[slnc 400]] Carol, who was rejected before, is now '
            'approved. [[slnc 500]] And no code changed. [[slnc 300]] '
            'That is handy in a test, but dangerous in production. [[slnc '
            "300]] So print the chain's order when the application "
            'starts.'
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
            'Last demo: what if nobody answers? [[slnc 400]] When every '
            'check has no opinion, a fallback decides. [[slnc 400]] It is '
            'a named setting. [[slnc 300]] By default, it approves, so '
            'Asha goes through. [[slnc 300]] Change it to refer, and Asha '
            'is sent to a person instead. [[slnc 500]] Reaching the end '
            'of a chain should be a decision, not an accident.'
        ),
    ),
    dict(
        key='10-verdict', kind='bullets', title='The Verdict',
        body=['Cheap and decisive links first.', '', 'Decide what a throwing link means.', '', 'Print the order at startup.', '', 'Test the whole chain.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Put the cheap, '
            'decisive checks first. [[slnc 300]] Decide what a crashing '
            "check should mean. [[slnc 300]] Print the chain's order when "
            'the application starts. [[slnc 300]] And test the whole '
            'chain, not just each check.'
        ),
    ),
    dict(
        key='11-recognise', kind='bullets', title='How To Recognise It',
        body=['A List of an interface in a', 'constructor, with Order on the', 'implementations.', '', 'A loop that stops at the first answer.'],
        narration=(
            'How can you spot this in code someone else wrote? [[slnc '
            '400]] Look for a constructor that receives a list of one '
            'interface. [[slnc 300]] With the at Order annotation on each '
            'implementation. [[slnc 300]] And a loop that stops at the '
            'first answer.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=["Servlet filters, Spring Security's", 'filter chain and validation', 'pipelines.'],
        narration=(
            'Where have you met this before? [[slnc 300]] In servlet '
            "filters, in Spring Security's filter chain, and in "
            'validation pipelines.'
        ),
    ),
    dict(
        key='13-versions', kind='bullets', title='What Was Used',
        body=['Spring Boot 4.1.1.', '', 'No web server, no database,', 'no web starter.'],
        narration=(
            'For the record, here are the versions. [[slnc 300]] Spring '
            'Boot four point one point one. [[slnc 300]] No web server, '
            'no database, and no web library.'
        ),
    ),
    dict(
        key='14-real', kind='bullets', title='What Is Real Here',
        body=["Everything is real: Spring's", 'container and its ordering.', '', 'The paid service is counted, not', 'really paid.'],
        narration=(
            "A quick, honest note about this demo. [[slnc 300]] Spring's "
            'container, and its ordering, are real. [[slnc 300]] The paid '
            'fraud service is only a counter. [[slnc 300]] Nothing is '
            'really paid for.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['For two checks that never change,', 'an if statement is clearer.'],
        narration=(
            'So, when is this too much? [[slnc 400]] For two checks that '
            'never change, a plain if statement is clearer than a chain.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Give two checks the same order', 'number and see what happens.'],
        narration=(
            "That's Chain of Responsibility with Spring. [[slnc 400]] If "
            'you remember one sentence, make it this one. [[slnc 300]] '
            'Spring builds and orders the chain for you, and that order '
            'becomes a cost you have to watch. [[slnc 500]] The full '
            'source code, written notes, diagrams, and an animated '
            'walkthrough are all in the repository. [[slnc 500]] Here is '
            'one exercise to try. [[slnc 300]] Give two checks the same '
            'order number. [[slnc 300]] Then run it, and find out what '
            'happens. [[slnc 500]] If this helped, a like really does '
            'help other people find it. [[slnc 300]] And subscribe, if '
            "you'd like the rest of the series. [[slnc 400]] Thanks for "
            'watching.'
        ),
    ),
]
