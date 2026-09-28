"""Scene definitions for the Mediator teaching video.

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
        title="Mediator",
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Mediator pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] When a group of objects all '
            'affect each other, you have two choices. [[slnc 300]] '
            'Connect every object to every other one. [[slnc 300]] Or '
            'give them all one single object to talk to, which holds the '
            'rules. [[slnc 300]] That single object is the mediator. '
            '[[slnc 600]] Think of an airport control tower. [[slnc 300]] '
            'Planes do not talk to each other. [[slnc 300]] They all talk '
            'to the tower, and the tower tells each one what to do. '
            '[[slnc 700]] In this video, we build the checkout page of an '
            'online shop. [[slnc 300]] Choosing a delivery country '
            'changes the couriers, the gift wrapping, the total, and '
            'whether you may place the order at all. [[slnc 500]] By the '
            'end, you will know why five controls can need nine '
            'connections, what that costs, and the one fair criticism of '
            'this pattern.'
        ),
    ),
    dict(
        key="02-scenario",
        kind="bullets",
        title="The Scenario",
        body=[
            "The checkout page of an online shop. Five controls:",
            "",
            "    Country          where the order is going",
            "    Shipping         a courier that serves that country",
            "    Gift wrap        hand-wrapped in London — domestic only",
            "    Total            the price, read-only",
            "    Place Order      pressable once it is all filled in",
            "",
            "Four rules connect them:",
            "",
            "  country  ->  which couriers exist",
            "  country  ->  whether gift wrap is offered at all",
            "  shipping + gift wrap  ->  the total",
            "  country + shipping    ->  can the button be pressed",
        ],
        narration=(
            "Here is the scenario: an online shop's checkout page, with "
            'five controls. [[slnc 400]] The delivery country. [[slnc '
            '200]] The courier. [[slnc 200]] A gift wrap option. [[slnc '
            '200]] The total. [[slnc 200]] And the place order button. '
            '[[slnc 600]] These five are connected by four rules. [[slnc '
            '400]] One. [[slnc 200]] Changing the country changes the '
            'list of couriers, because different couriers serve different '
            'countries. [[slnc 300]] Two. [[slnc 200]] Gift wrapping is '
            'done by hand in the London warehouse, so it is only offered '
            'for UK orders. [[slnc 300]] Three. [[slnc 200]] The total '
            'follows the courier and the gift wrap. [[slnc 300]] And '
            'four. [[slnc 200]] The button may only be pressed when a '
            'country and a courier are both chosen. [[slnc 600]] The '
            'rules are simple. [[slnc 300]] The hard part is where they '
            'live.'
        ),
    ),
    dict(
        key="03-anatomy",
        kind="bullets",
        title="Look Closely at One Click",
        body=[
            "The shopper has a UK order: Express shipping, gift wrapped, £48.",
            "",
            "Then they change the country to US.",
            "",
            "    gift wrap:  offered = false      <- correctly withdrawn",
            "    gift wrap:  ticked  = true       <- nobody cleared it",
            "",
            "    Total: £42     — and £2 of that is wrapping",
            "                     the London warehouse will never do.",
            "",
            "Nothing throws. Nothing logs.",
            "The shopper is simply charged for a service they cannot receive.",
        ],
        narration=(
            "Before any code, let's follow one click. [[slnc 400]] A "
            'shopper has a UK order, with express shipping, gift wrapped, '
            'for forty-eight pounds. [[slnc 300]] Then they change the '
            'country to the United States. [[slnc 500]] The gift wrap '
            'option is correctly withdrawn, because the London warehouse '
            'cannot wrap this order. [[slnc 300]] But the tick stays in '
            'the box. [[slnc 300]] Withdrawing the option and clearing '
            'the tick were two separate steps, and only one was written. '
            '[[slnc 500]] So the total is now forty-two pounds. [[slnc '
            '300]] And two pounds of that is for gift wrapping that will '
            'never happen. [[slnc 600]] Nothing crashes, and nothing is '
            'logged. [[slnc 300]] It looks like a normal checkout, with '
            'two pounds of pure fiction in it.'
        ),
    ),
    dict(
        key="04-problem",
        kind="code",
        title="The Naive Approach — Everyone Wires Everyone",
        body="""country.wire(shipping, giftWrap, total, placeOrder);   // 4
shipping.wire(giftWrap, total, placeOrder);            // 3
giftWrap.wire(shipping, total);                        // 2
                                                       // 9 references

public void select(String country) {           // inside NaiveCountry
    this.country = country;
    shipping.showOptions(...);                 // remembered
    giftWrap.setAvailable(...);                // remembered — half of it
    total.recalculate(shipping, giftWrap);     // remembered
                                               // button: forgotten
}""",
        narration=(
            'Here is why it happens. [[slnc 400]] The obvious place for '
            'the rule, when the country changes, refresh the couriers, is '
            'inside the country control. [[slnc 300]] So the country '
            'control is given a reference to the courier control. [[slnc '
            '400]] But gift wrap depends on the country too, so it needs '
            'that as well. [[slnc 300]] And the total changes, so it '
            'needs the total. [[slnc 300]] And the button might need '
            'checking, so it needs the button. [[slnc 500]] That makes '
            'nine references, on a page with just five controls. [[slnc '
            "500]] Inside the country control's method, three of the four "
            'follow-up steps were remembered. [[slnc 300]] The fourth, '
            're-checking the button, was forgotten. [[slnc 600]] Nobody '
            'was careless. [[slnc 300]] The page is only correct if '
            'someone holds all five controls in their head, every time '
            'they change any one of them.'
        ),
    ),
    dict(
        key="05-why-hurts",
        kind="bullets",
        title="Why That Hurts",
        body=[
            "1.  Nobody can see the whole form.",
            "    'What happens when the country changes?' is spread",
            "    across three files, and no file has the answer.",
            "",
            "2.  The bugs are OMISSIONS. You cannot review a line",
            "    that was never written.",
            "",
            "3.  The wiring grows faster than the form:",
            "        3 controls -> 6      5 controls -> 20",
            "                    10 controls -> 90",
            "",
            "4.  No widget can be built or tested on its own.",
            "    And shipping holds gift wrap, which holds shipping.",
        ],
        narration=(
            'So what exactly is wrong? [[slnc 300]] Four separate things. '
            '[[slnc 500]] One. [[slnc 200]] Nobody can see the whole '
            'form. [[slnc 300]] What happens when the country changes is '
            'spread across three files, and no single file has the '
            'answer. [[slnc 500]] Two. [[slnc 200]] The bugs are missing '
            'lines. [[slnc 300]] And you cannot review a line that was '
            'never written. [[slnc 500]] Three. [[slnc 200]] The '
            'connections grow faster than the form. [[slnc 300]] Three '
            'controls can have six connections. [[slnc 300]] Five '
            'controls, twenty. [[slnc 300]] Ten controls, ninety. [[slnc '
            '500]] And four. [[slnc 200]] No control can be built or '
            'tested alone. [[slnc 300]] The country control needs four '
            'other controls just to exist.'
        ),
    ),
    dict(
        key="06-pattern",
        kind="quote",
        title="The Mediator Pattern",
        # One line per rendered line: kind_quote lays these out as-is.
        body=[
            "Define an object that encapsulates how a set of",
            "objects interact. Mediator promotes loose coupling",
            "by keeping objects from referring to each other",
            "explicitly, and it lets you vary their interaction",
            "independently.",
            "",
            "— Gang of Four",
            "",
            "In plain terms:",
            "the parts stop talking to each other,",
            "and the rules move somewhere you can read them.",
        ],
        narration=(
            "Here is the pattern's definition, from the famous Gang of "
            'Four book. [[slnc 400]] Define an object that encapsulates '
            'how a set of objects interact, and keep the objects from '
            'referring to each other directly. [[slnc 600]] That has two '
            'halves. [[slnc 300]] Keeping objects from referring to each '
            'other is the mechanism. [[slnc 300]] Nine references become '
            'five. [[slnc 500]] Encapsulating how they interact is the '
            'bigger benefit. [[slnc 300]] After the change, there is one '
            'file, with one method, that tells you everything the page '
            'does. [[slnc 300]] Nothing hides anywhere else.'
        ),
    ),
    dict(
        key="07-analogy",
        kind="bullets",
        title="An Analogy",
        body=[
            "Aircraft near an airport.",
            "",
            "  They do not negotiate with each other.",
            "  They all talk to the tower.",
            "",
            "Not because pilots can't be trusted —",
            "because n aircraft talking to each other is n² conversations,",
            "and one of them will be missed.",
            "",
            "One tower is n conversations,",
            "and the rules of the airspace are in one head.",
        ],
        narration=(
            'Here is the analogy to hold on to: aircraft near an airport. '
            '[[slnc 500]] Planes do not negotiate with each other about '
            'who lands first. [[slnc 300]] They all talk to the control '
            'tower. [[slnc 300]] The tower knows where everyone is, and '
            'tells each plane what to do. [[slnc 600]] That is not '
            'because pilots cannot be trusted. [[slnc 300]] It is simple '
            'arithmetic. [[slnc 300]] Ten planes talking to each other '
            'means ninety conversations, and sooner or later, one is '
            'missed. [[slnc 300]] Ten planes talking to one tower means '
            'just ten conversations. [[slnc 300]] And all the rules are '
            'in one place. [[slnc 500]] In our project, the checkout form '
            'is the tower, and the five controls are the planes.'
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="The Roles",
        body=None,
        narration=(
            'So here are the pieces. [[slnc 500]] The Checkout Mediator '
            'interface has exactly one method, called changed. [[slnc '
            '300]] A control calls it to say, something about me changed. '
            '[[slnc 300]] Controls report. [[slnc 300]] They never ask. '
            '[[slnc 500]] Every control extends a base class called Form '
            'Widget. [[slnc 300]] It has two fields: a name, and the '
            'mediator. [[slnc 300]] There is no field that could hold '
            'another control. [[slnc 300]] So controls cannot tangle, '
            'even by accident. [[slnc 500]] Then there are the five real '
            'controls: country, courier, gift wrap, the total, and the '
            'button. [[slnc 300]] Each one knows the form. [[slnc 300]] '
            'And the form knows all five. [[slnc 500]] The shape is a '
            'star, not a web.'
        ),
    ),
    dict(
        key="09-colleague",
        kind="code",
        title="The Colleague — Notice What Is Missing",
        body="""public abstract class FormWidget {
    private final String name;
    private final CheckoutMediator mediator;    // its ONLY reference

    protected void announceChange() {
        mediator.changed(this);
    }
}

public class CountrySelector extends FormWidget {
    public void select(String country) {
        this.country = country;
        announceChange();          // "something about me changed"
    }                              // ...and that is the whole class
}""",
        narration=(
            "Let's look at a control, and notice what is missing. [[slnc "
            '500]] The base class has only two fields: a name, and the '
            'mediator. [[slnc 300]] No field can hold another control. '
            '[[slnc 500]] Now the country control. [[slnc 300]] When a '
            'country is chosen, it stores the country, announces that it '
            'changed, and stops. [[slnc 300]] That is the whole class. '
            '[[slnc 500]] Compare it with the naive version, which had '
            'four follow-up steps, and still missed one. [[slnc 500]] A '
            'control now only says, something about me is different. '
            '[[slnc 300]] What that means for the rest of the page is not '
            'its business.'
        ),
    ),
    dict(
        key="10-mediator",
        kind="code",
        title="The Mediator — The Whole Page, in One Method",
        body="""@Override
public void changed(FormWidget source) {

    if (source == country) {                  // the only branch
        shipping.showOptions(methodsFor(country.country()));
        giftWrap.setAvailable(isDomestic(country.country()));
    }

    refreshTotal();       // every time, whatever changed
    refreshButton();      // every time, whatever changed
}

void setAvailable(boolean available) {        // on GiftWrapCheckbox
    this.available = available;
    if (!available) this.ticked = false;      // one call, both facts
}""",
        narration=(
            'And here is the whole page, in one method, in the mediator. '
            '[[slnc 500]] If the country changed, it refreshes the '
            'courier list, and sets whether gift wrap is offered. [[slnc '
            '300]] Then, whatever changed, it recalculates the total, and '
            're-checks the button. [[slnc 600]] Two things are worth '
            'noticing. [[slnc 400]] First, the total and the button are '
            'refreshed after every change, with no special cases. [[slnc '
            '300]] So the mediator never needs to remember that clearing '
            'the courier affects the button. [[slnc 300]] It simply '
            'checks again, every time. [[slnc 300]] Simple and always '
            'right beats clever and sometimes wrong. [[slnc 500]] Second, '
            'withdrawing the gift wrap offer also clears the tick, in the '
            'same method. [[slnc 300]] There is no way to do only half of '
            'that. [[slnc 300]] So there is nothing left to forget. '
            '[[slnc 500]] One if statement. [[slnc 300]] That is the '
            'entire control flow of the page.'
        ),
    ),
    dict(
        key="11-proof",
        kind="code",
        title="The Tests — Asserting the Structure, Not Just the Behaviour",
        body="""@Test void widgetsOnlyKnowTheMediator() {
    for (FormWidget widget : allFiveWidgets) {
        for (Field field : allFieldsOf(widget.getClass())) {
            if (FormWidget.class.isAssignableFrom(field.getType()))
                offenders.add(widget.name() + "." + field.getName());
        }
    }
    assertEquals(List.of(), offenders);      // no widget holds a widget
}

@Test void chargesForWrappingItWillNotDo() {     // the NAIVE form
    naive.country().select("US");
    assertTrue(naive.giftWrap().isTicked());     // the wrong answer,
    assertEquals(42, naive.total().pounds());    // pinned on purpose
}""",
        narration=(
            'The project has fourteen tests. [[slnc 300]] Two of them '
            'prove the pattern. [[slnc 500]] A test like, choosing '
            'express makes the total forty-six pounds, passes for the '
            'tangled version too. [[slnc 300]] So it proves nothing about '
            'the pattern. [[slnc 500]] The first special test checks the '
            'structure. [[slnc 300]] It looks at every field of every '
            'control, and fails if any field can hold another control. '
            '[[slnc 300]] A comment saying, controls must not reference '
            'each other, lasts until the first person in a hurry. [[slnc '
            '300]] This test does not. [[slnc 500]] The second test '
            'checks a wrong answer, on purpose. [[slnc 300]] It confirms '
            'that the naive form still has the bug: the tick stays, and '
            'the total is forty-two pounds. [[slnc 300]] The cost of that '
            'design is stated out loud, by the build.'
        ),
    ),
    dict(
        key="12-output",
        kind="console",
        title="Running It",
        body="""$ ./gradlew run

=== every widget wired to every other ===
UK, Express, gift wrapped        Total: £48   place order: enabled
shopper changes the country to US
  shipping chosen : (none)
  gift wrap       : offered=false, ticked=true    <- still ticked
  Total: £42                     <- £2 of wrapping that won't happen
  place order     : enabled      <- no courier, and it lets them through

=== every widget wired to the mediator ===
UK, Express, gift wrapped        Total: £48   place order: enabled
shopper changes the country to US
  gift wrap       : offered=false, ticked=false   <- cleared with it
  Total: £40                     <- basket only, nothing chosen yet
  place order     : disabled     <- the form re-checked itself""",
        narration=(
            "Let's run the demo. [[slnc 400]] The same page, the same "
            'three clicks, and the same change of mind. [[slnc 500]] '
            'First, the tangled version. [[slnc 300]] The total is '
            'forty-two pounds, with two pounds of phantom gift wrap. '
            '[[slnc 300]] And the place order button still works, even '
            'though no courier is chosen. [[slnc 500]] Now the mediated '
            'version. [[slnc 300]] The tick disappeared when the offer '
            'did. [[slnc 300]] The courier was cleared, so the total is '
            'back to just the basket. [[slnc 300]] And the button '
            'switched itself off. [[slnc 600]] Notice that nobody wrote '
            'code saying, when the country changes, disable the button. '
            '[[slnc 300]] It just happens, because the mediator re-checks '
            'everything after every change.'
        ),
    ),
    dict(
        key="13-wrapup",
        kind="bullets",
        title="What to Remember",
        body=[
            "When everything talks to everything, nobody sees the whole thing.",
            "Give them one place to talk to, and the rules have somewhere to live.",
            "",
            "  Mediator   colleagues know it; it knows all of them",
            "  Observer   the publisher knows NOTHING about its subscribers",
            "  Facade     faces outward, to simplify life for a caller",
            "",
            "A publisher could not disable a button because a",
            "drop-down was cleared. A mediator can. That is the job.",
            "",
            "The honest cost: everything you take out of the widgets",
            "goes INTO the mediator. Split it before it becomes",
            "the class nobody wants to open.",
        ],
        narration=(
            'So, what should you remember? [[slnc 400]] When everything '
            'talks to everything, nobody can see the whole picture. '
            '[[slnc 300]] Give them one place to talk to, and the rules '
            'have somewhere to live. [[slnc 600]] People often confuse '
            'Mediator with Observer. [[slnc 300]] The difference is '
            "knowledge. [[slnc 300]] An observer's publisher knows "
            'nothing about its subscribers. [[slnc 300]] A mediator knows '
            'all of its controls, on purpose. [[slnc 300]] That knowledge '
            'is what lets it enforce a rule that spans several of them. '
            '[[slnc 500]] A Facade also sits in front of several objects. '
            '[[slnc 300]] But a facade faces outward, to make life '
            'simpler for an outside caller. [[slnc 300]] A mediator faces '
            'inward. [[slnc 600]] Now the honest cost, and this criticism '
            'is fair. [[slnc 300]] Everything you take out of the '
            'controls goes into the mediator. [[slnc 300]] On a real '
            'form, that class can grow huge. [[slnc 300]] The answer is '
            'to split it, one mediator per section of the page, before it '
            'gets there. [[slnc 500]] And for two controls that will '
            'never be three, direct wiring is clearer. [[slnc 300]] This '
            'pattern pays off at about four or five interacting parts.'
        ),
    ),
    dict(
        key="14-outro",
        kind="outro",
        title="Thanks for Watching",
        body=[
            "Full source, notes, diagrams and an animated walkthrough",
            "are in the repository — including the exercise that gives",
            "one widget a reference to another, and watches a test name it.",
        ],
        narration=(
            "That's the Mediator pattern. [[slnc 400]] If you remember "
            'one sentence, make it this one. [[slnc 300]] Give a group of '
            'objects one place to talk to, and their rules have one place '
            'to live. [[slnc 500]] The full source code, written notes, '
            'diagrams, and an animated walkthrough are all in the '
            'repository. [[slnc 500]] Here is one exercise to try. [[slnc '
            '300]] Give the country control a field that points at the '
            'total. [[slnc 300]] Run the tests, and listen as the '
            'structure test names that field. [[slnc 500]] If this '
            'helped, a like really does help other people find it. [[slnc '
            "300]] And subscribe, if you'd like the rest of the series. "
            '[[slnc 400]] Thanks for watching.'
        ),
    ),
]
