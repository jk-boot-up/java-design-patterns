"""Scene definitions for the MVP and MVVM teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='MVP and MVVM',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the M V '
            'P and M V V M patterns, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] Both patterns take the rules '
            'out of the screen. [[slnc 400]] In M V P, which stands for '
            'Model, View, Presenter, a presenter tells a passive screen '
            'exactly what to show. [[slnc 400]] In M V V M, which stands '
            'for Model, View, View Model, the screen connects itself to '
            'some state, and updates whenever that state changes. [[slnc '
            '600]] Think of a stage play. [[slnc 300]] In M V P, a '
            'director stands in the wings and tells each actor every '
            'move. [[slnc 300]] In M V V M, the actors watch a '
            'scoreboard, and react to it by themselves. [[slnc 700]] In '
            'our online store, the cart screen shows a total, an item '
            'count, and a checkout button. [[slnc 300]] Right now, the '
            'rules for those are tangled into the screen. [[slnc 500]] In '
            'this video, we untangle them both ways, and then compare the '
            'costs.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['The cart screen shows a total,', 'an item count,', 'and a checkout button.', '', 'The button is on only when', 'the cart is not empty.', '', 'Where do these rules live?'],
        narration=(
            'Here is the scenario. [[slnc 400]] The cart screen shows '
            'three things. [[slnc 300]] The total price. [[slnc 200]] The '
            'number of items. [[slnc 200]] And a checkout button. [[slnc '
            '400]] The checkout button is switched on only when the cart '
            'is not empty. [[slnc 500]] So here is the question. [[slnc '
            '300]] Where should these rules live?'
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
            'First, the old way: the screen decides everything. [[slnc '
            '400]] To check the total, and the checkout rule, we had to '
            'create a real screen. [[slnc 300]] One window was opened, '
            'just to run a test. [[slnc 500]] The rules are welded to the '
            "screen's buttons and labels."
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['Keep the rules out of the', 'screen.', '', 'MVP: a presenter tells a', 'passive view what to show.', '', 'MVVM: a view model keeps', 'state, and the view binds to it.'],
        narration=(
            'Now, the pattern. [[slnc 400]] Keep the rules out of the '
            'screen. [[slnc 500]] In M V P, a presenter holds the rules. '
            '[[slnc 300]] It tells a passive screen what to show. [[slnc '
            '500]] In M V V M, a view model holds the rules and the '
            'state. [[slnc 300]] The screen connects to that state once, '
            'and follows it from then on. [[slnc 300]] This connecting is '
            'called binding.'
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
            'Second demo: M V P, where a presenter tells a passive '
            'screen. [[slnc 400]] We add two items to the cart. [[slnc '
            '400]] The presenter then gives the screen three '
            'instructions. [[slnc 300]] Show the total, twenty-five '
            'pounds fifty. [[slnc 300]] Show the count, two. [[slnc 300]] '
            'And switch the checkout button on. [[slnc 500]] How many '
            'windows were opened? [[slnc 300]] None. [[slnc 400]] The '
            'rules were checked with no screen at all, using a fake view.'
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
            'Third demo: the screen makes no decisions. [[slnc 400]] With '
            'an empty cart, the presenter says: total zero, count zero, '
            'checkout off. [[slnc 500]] Now add one item, then remove it '
            "again. [[slnc 300]] The presenter's last three instructions "
            'are exactly the same. [[slnc 400]] The presenter decided '
            'that checkout is off again. [[slnc 300]] The screen just '
            'obeys.'
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
            'Fourth demo: M V V M, where the screen binds to state. '
            '[[slnc 400]] The screen starts by showing zero, no items, '
            'and checkout off. [[slnc 400]] We add two items. [[slnc '
            '300]] The screen now shows twenty-five pounds fifty, two '
            'items, and checkout on. [[slnc 500]] Nobody told the screen '
            'to update. [[slnc 300]] It bound to the view model once, at '
            'the start. [[slnc 400]] And the view model holds no '
            'reference to any screen at all.'
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
            'Fifth demo: many screens, one view model. [[slnc 400]] A '
            'phone screen and a watch screen both bind to the same view '
            'model. [[slnc 400]] Both show sixteen pounds, one item, and '
            'checkout on. [[slnc 500]] Adding that second screen needed '
            'no change to the view model at all.'
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
            'Finally, the costs of each. [[slnc 500]] In M V V M, imagine '
            'a screen that forgot to bind the total. [[slnc 300]] It '
            'shows a question mark. [[slnc 300]] Nothing fails, and no '
            'error appears. [[slnc 300]] It is simply wrong. [[slnc 500]] '
            "In M V P, the screen's interface has three methods. [[slnc "
            '300]] Every new item on the screen adds another method, to '
            'the interface, the presenter, and every screen. [[slnc 500]] '
            'So M V V M hides the wiring inside the binding. [[slnc 300]] '
            'And M V P spells every step out, and grows long.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['A Presenter that holds a View', 'interface.', '', 'A ViewModel with observable', 'properties, LiveData, StateFlow or', '', 'Data binding in WPF, Android,', 'SwiftUI or Angular.'],
        narration=(
            'How can you spot these patterns in code someone else wrote? '
            '[[slnc 400]] For M V P, look for a presenter that holds a '
            'view interface. [[slnc 300]] And a view implemented by a '
            'fake, in tests. [[slnc 400]] For M V V M, look for a view '
            'model with observable properties. [[slnc 300]] Names like '
            'Live Data, State Flow, or Observable Field. [[slnc 300]] And '
            'data binding in frameworks like W P F, Android, Swift U I, '
            'or Angular.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Take the rules out of the screen', 'either way. Use MVP when you want', 'every step visible and easy to', 'check with a fake view. Use MVVM', 'when your platform has good', 'binding, and several screens share', 'one state. Test the presenter or', 'the view model with no screen, and', 'check the bindings too.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Either way, take the '
            'rules out of the screen. [[slnc 500]] Choose M V P when you '
            'want every step visible, and easy to check with a fake '
            'screen. [[slnc 400]] Choose M V V M when your platform has '
            'good binding, and several screens share one state. [[slnc '
            '500]] And in both cases, test the presenter or the view '
            'model with no screen. [[slnc 300]] Then check the bindings '
            'too.'
        ),
    ),
    dict(
        key='12-real', kind='bullets', title='What Is Real Here',
        body=['Everything is plain Java.', '', 'Every number quoted comes from', "this program's own output.", '', 'Nothing depends on a clock,', 'so every run is the same.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 300]] '
            'Everything is plain Java. [[slnc 300]] Every number you '
            "heard comes from the program's own output. [[slnc 300]] And "
            'nothing depends on the clock, so every run gives the same '
            'result.'
        ),
    ),
    dict(
        key='13-too-much', kind='bullets', title='When This Is Too Much',
        body=['For a static page, or a screen', 'with two fields, the extra layer', 'is more than the problem. Keep it', 'for screens with rules that you', 'want to check on their own.'],
        narration=(
            'So, when is this too much? [[slnc 400]] For a static page, '
            'or a screen with just two fields, the extra layer is bigger '
            'than the problem. [[slnc 400]] Keep it for screens with '
            'rules that you want to check on their own.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's M V P and M V V M. [[slnc 400]] If you remember one "
            'sentence, make it this one. [[slnc 300]] Both keep the rules '
            'out of the screen, and the price is a longer interface on '
            'one side, and hidden wiring on the other. [[slnc 500]] The '
            'full source code, written notes, diagrams, and an animated '
            'walkthrough are all in the repository. [[slnc 500]] Here is '
            'one exercise to try. [[slnc 300]] Add a warning that appears '
            'when the total is over five hundred pounds. [[slnc 300]] '
            'Build it first in the presenter, and then in the view model. '
            '[[slnc 500]] If this helped, a like really does help other '
            "people find it. [[slnc 300]] And subscribe, if you'd like "
            'the rest of the series. [[slnc 400]] Thanks for watching.'
        ),
    ),
]
