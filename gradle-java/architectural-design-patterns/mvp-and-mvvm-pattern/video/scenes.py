"""Scene definitions for the MVP and MVVM teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='MVP and MVVM',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the MVP and MVVM '
            'pattern in Java, and it is written and presented by '
            'Jayasekhar Konduru. [[slnc 300]] The plain definition: M V P '
            'and M V V M both take the rules out of the screen. In M V P, '
            'a presenter tells a passive view what to show. In M V V M, '
            'the view binds to state that a view model keeps up to date. '
            '[[slnc 350]] This is another project in the architecture '
            'category, whose subject is how a whole application is '
            'arranged, and who may depend on whom. In our online store, '
            'the cart screen shows a total, a count and a checkout '
            'button, and the rules for them are tangled into the screen. '
            '[[slnc 300]] By the end you will see a screen whose rules '
            'cannot be checked without opening a window, see a presenter '
            'tell a passive view, see the view make no decisions, see a '
            'view bind to state, see two screens share one view model, '
            'and see the bill, which is a long interface on one side and '
            'hidden wiring on the other.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['The cart screen shows a total,', 'an item count,', 'and a checkout button.', '', 'The button is on only when', 'the cart is not empty.', '', 'Where do these rules live?'],
        narration=(
            'Here is the scenario. The cart screen shows a total, an item '
            'count, and a checkout button. The button is on only when the '
            'cart is not empty. [[slnc 300]] The question: where do these '
            'rules live?'
        ),
    ),
    dict(
        key='03-fat', kind='console', title='The Screen Decides',
        body="""ONE. The screen decides.
  to check the total and the
  checkout rule, a screen was
  needed.
  windows opened: 1.

  the rules are welded to the
  widgets.""",
        narration=(
            'First, the screen decides. To check the total and the '
            'checkout rule, a screen was needed. One window was opened. '
            'The rules are welded to the widgets.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['Keep the rules out of the', 'screen.', '', 'MVP: a presenter tells a', 'passive view what to show.', '', 'MVVM: a view model keeps', 'state, and the view binds to it.'],
        narration=(
            'The pattern. Keep the rules out of the screen. In M V P, a '
            'presenter tells a passive view what to show. In M V V M, a '
            'view model keeps state, and the view binds to it.'
        ),
    ),
    dict(
        key='05-mvp', kind='console', title='A Presenter Tells A Passive View',
        body="""TWO. MVP.
  after two adds the view was
  told: total 25.50, count 2,
  checkout on.

  windows opened: 0.
  the rules were checked with
  no screen.""",
        narration=(
            'Second, M V P: a presenter tells a passive view. After two '
            'adds, the view was told: show the total, twenty five pounds '
            'fifty; show the count, two; enable checkout. Windows opened: '
            'none. The rules were checked with no screen.'
        ),
    ),
    dict(
        key='06-passive', kind='console', title='The View Makes No Decisions',
        body="""THREE. A passive view.
  empty cart: total 0, count 0,
  checkout off.
  add then remove: the same.

  the presenter decides.
  the view just obeys.""",
        narration=(
            'Third, the view makes no decisions. An empty cart: total '
            'zero, count zero, checkout off. Add one item and remove it, '
            'and the last three calls are the same. The presenter decides '
            'that checkout is off again. The view just obeys.'
        ),
    ),
    dict(
        key='07-mvvm', kind='console', title='The View Binds To State',
        body="""FOUR. MVVM.
  start: 0.00 | 0 items | off.
  after two adds:
  25.50 | 2 items | on.

  nobody told the screen.
  it bound once.
  the view model has no view.""",
        narration=(
            'Fourth, M V V M: the view binds to state. The screen starts '
            'as zero, no items, checkout off. After two adds it shows '
            'twenty five pounds fifty, two items, checkout on. Nobody '
            'told the screen. It bound once. The view model holds no '
            'reference to any view.'
        ),
    ),
    dict(
        key='08-many', kind='console', title='Many Views, One View Model',
        body="""FIVE. Many views.
  phone: 16.00 | 1 item | on.
  watch: 16.00 | 1 item | on.

  a second screen cost no
  change to the view model.""",
        narration=(
            'Fifth, many views, one view model. A phone screen and a '
            'watch screen bind to the same view model. Both show sixteen '
            'pounds, one item, checkout on. A second screen cost no '
            'change to the view model.'
        ),
    ),
    dict(
        key='09-bill', kind='console', title='The Bill',
        body="""SIX. The bill.
  MVVM: a screen forgot to bind
  the total. it draws ?.
  nothing failed.

  MVP: the view interface has 3
  methods; each new widget adds
  one, everywhere.

  MVVM hides the wiring.
  MVP spells it out.""",
        narration=(
            'Last, the bill. In M V V M, a screen that forgot to bind the '
            'total draws a question mark. Nothing failed. It is just '
            'wrong. In M V P, the view interface has three methods, and '
            'each new thing on the screen adds one to the interface, the '
            'presenter, and every view. M V V M hides the wiring in the '
            'binding. M V P spells it out, and gets long.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['A Presenter that holds a View', 'interface.', '', 'A ViewModel with observable', 'properties, LiveData, StateFlow or', '', 'Data binding in WPF, Android,', 'SwiftUI or Angular.'],
        narration=(
            'How do you recognise this in code you did not write? A '
            'Presenter that holds a View interface. A ViewModel with '
            'observable properties, LiveData, StateFlow or '
            'ObservableField. Data binding in WPF, Android, SwiftUI or '
            'Angular. A View implemented by a test double.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Take the rules out of the screen', 'either way. Use MVP when you want', 'every step visible and easy to', 'check with a fake view. Use MVVM', 'when your platform has good', 'binding, and several screens share', 'one state. Test the presenter or', 'the view model with no screen, and', 'check the bindings too.'],
        narration=(
            'Here is my verdict, plainly. Take the rules out of the '
            'screen either way. Use MVP when you want every step visible '
            'and easy to check with a fake view. Use MVVM when your '
            'platform has good binding, and several screens share one '
            'state. Test the presenter or the view model with no screen, '
            'and check the bindings too.'
        ),
    ),
    dict(
        key='12-real', kind='bullets', title='What Is Real Here',
        body=['Everything is plain Java.', '', 'Every number quoted comes from', "this program's own output.", '', 'Nothing depends on a clock,', 'so every run is the same.'],
        narration=(
            'The same honest admission as everywhere in this course. '
            'Everything is plain Java. Every number quoted comes from '
            "this program's own output. Nothing depends on a clock, so "
            'every run is the same.'
        ),
    ),
    dict(
        key='13-too-much', kind='bullets', title='When This Is Too Much',
        body=['For a static page, or a screen', 'with two fields, the extra layer', 'is more than the problem. Keep it', 'for screens with rules that you', 'want to check on their own.'],
        narration=(
            'So when is it too much? For a static page, or a screen with '
            'two fields, the extra layer is more than the problem. Keep '
            'it for screens with rules that you want to check on their '
            'own.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's MVP and MVVM. [[slnc 250]] If you take one sentence "
            'away, take this one: M V P and M V V M keep the rules out of '
            'the screen, and the price is a longer interface on one side, '
            'and hidden wiring on the other. [[slnc 350]] The full '
            'source, the written notes, the diagrams and an animated '
            'walkthrough are all in the repository, running offline with '
            'nothing installed but a Java development kit. [[slnc 300]] '
            'If you try one exercise, add a warning line that shows when '
            'the total is over five hundred pounds, first in the '
            'presenter, then in the view model. [[slnc 300]] If this '
            'helped, a like genuinely does help other people find it, and '
            'subscribe if you would like the rest of the series. [[slnc '
            '250]] Thanks for watching.'
        ),
    ),
]
