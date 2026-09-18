"""Scene definitions for the MVC teaching video.

Each scene has:
  key        - short id, used for the generated file names
  title      - slide heading
  kind       - "poster" | "bullets" | "code" | "console" | "quote" | "diagram" | "outro"
  body       - content, meaning depends on kind
  narration  - the text spoken by the narrator (see narration.md)

Written to stand on its own with the screen off: architecture is described
as rules and directions in words, and no sentence says "as you can see".

This is the category's second project, one step from Layered Architecture:
the same shared feature, the same four steps underneath, and one new
question laid on top of it -- once an order is placed, who is allowed to
compute what a customer is shown.
"""

SCENES = [
    dict(
        key="01-poster",
        kind="poster",
        title="MVC",
        body=None,
        narration=(
            "Hello, and welcome. This video explains the Model View "
            "Controller pattern in Java, and it is written and presented by "
            "Jayasekhar Konduru. [[slnc 300]] Let's start with the plain "
            "definition. MVC splits a screen into three roles. A model "
            "holds data and does the one calculation that matters. A view "
            "turns that data into text or pixels and does no calculation of "
            "its own. And a controller takes an input and turns it into a "
            "call on the model, then tells a view to render. [[slnc 350]] "
            "Now, almost everyone who says those three words means something "
            "slightly different by them, and this video is going to be "
            "precise about that, because the version most of you have "
            "actually used at work is not quite the one taught in "
            "textbooks. [[slnc 300]] So this video builds a real working "
            "online shop -- the same order this whole course's category "
            "places -- and shows what happens when a screen and a "
            "confirmation email both need to show a customer the same "
            "total, and one of them decides to work it out for itself. "
            "[[slnc 300]] By the end you will know why that is not a typo "
            "or a rounding accident but a structural bug, what a model has "
            "to guarantee to make it impossible, and which flavour of MVC "
            "you have actually been using all along."
        ),
    ),
    dict(
        key="02-scenario",
        kind="bullets",
        title="The Scenario",
        body=[
            "The same order this whole category places.",
            "",
            "    Ada Okafor, customer cust-8801, buys:",
            "    1 Espresso Machine        £249.00",
            "    1 Burr Grinder             £89.50",
            "    2 Coffee Beans, 1kg        £44.00",
            "                       Total  £382.50",
            "",
            "Placed once. Shown twice: on screen, and by email.",
        ],
        narration=(
            "Same order as every project in this category. Ada Okafor buys "
            "an espresso machine, a burr grinder, and two bags of coffee "
            "beans, for three hundred and eighty-two pounds fifty. [[slnc "
            "300]] Stock is checked, the card is charged, the order is "
            "saved -- exactly the sequence the previous project in this "
            "series built and tested. This video picks up from the moment "
            "just after that. [[slnc 300]] Ada is shown a summary on "
            "screen. Ada also gets a confirmation email a moment later. "
            "Both of them are supposed to say three hundred and eighty-two "
            "pounds fifty. Hold onto that number, because for most of this "
            "video, one of the two outputs is not going to agree with it."
        ),
    ),
    dict(
        key="03-no-separation",
        kind="code",
        title="Version One — No Separation At All",
        body="""public class EverythingOrderScreen {

    public String checkout(Map<String,Integer> w) {
        // check stock, take payment,
        // AND format the screen text --
        // all in this one method.
    }
}
// works. and untestable without a full checkout.""",
        narration=(
            "Before there is a model to separate from a view, there has to "
            "be no separation at all, so that is where the project starts. "
            "[[slnc 300]] One class checks stock, takes payment, and "
            "formats the screen text, in the same method. It works, and it "
            "has exactly one property worth noticing: because there is only "
            "one method, the checkout and the screen text cannot possibly "
            "disagree with each other -- there is only one calculation, "
            "full stop. [[slnc 350]] Its problem is a different one. Try to "
            "write a test that only checks 'does the summary read "
            "correctly' without running a full checkout alongside it. You "
            "cannot, because they are the same fourteen lines. That is the "
            "cost of no separation. The cost of the wrong kind of "
            "separation, which is what act three shows you, is worse."
        ),
    ),
    dict(
        key="04-three-roles",
        kind="bullets",
        title="Three Roles",
        body=[
            "Model",
            "    holds the order's lines and its ONE total",
            "",
            "View",
            "    turns the model into text. computes nothing.",
            "",
            "Controller",
            "    places the order, builds the model,",
            "    hands it to whichever views are asked for",
        ],
        narration=(
            "So here are the three roles, and I want to name what each one "
            "is not allowed to know, because that is the actual "
            "architecture. [[slnc 300]] The model holds the placed order's "
            "lines, and its one total. It does not know how it will be "
            "displayed -- on a screen, in an email, or in a format nobody "
            "has invented yet. [[slnc 300]] The view turns that model into "
            "text. It computes nothing. Not a sum, not a rounding, not a "
            "percentage -- if a view contains an arithmetic operator applied "
            "to a price, something has already gone wrong. [[slnc 350]] And "
            "the controller places the order, reads it back from storage, "
            "builds exactly one model from it, and hands that same model to "
            "whichever views were asked for. [[slnc 300]] Here is the "
            "sentence I want you to leave this video with, stated early "
            "because everything else demonstrates it. Two views cannot "
            "disagree about a number neither of them is allowed to "
            "calculate."
        ),
    ),
    dict(
        key="05-shortcut",
        kind="console",
        title="The Shortcut",
        body="""THREE. A second view, the shortcut way.
  Total: £382.50
  Thank you. Your order ord-1001 for
  £383.00 is confirmed.

  the screen says £382.50. the email says £383.00.
  NOTHING IN THE BUILD OBJECTED.""",
        narration=(
            "Now here is the moment this video is actually about. [[slnc "
            "300]] A real screen exists, reading a real model, and it "
            "works. Somebody is then asked for a confirmation email. The "
            "model does not have a convenient method yet for 'unit prices "
            "rounded to the nearest pound, for a tidier-looking line', so "
            "rather than ask for one, the new email view reaches straight "
            "into the product catalogue itself, and rounds each unit price "
            "before multiplying. [[slnc 350]] It compiles. It is not a "
            "hack -- a reviewer would see a small, self-contained view doing "
            "its own formatting, and approve it. [[slnc 300]] And it prints "
            "a different total. The burr grinder is eighty-nine pounds "
            "fifty. Rounded to the nearest pound before it is multiplied by "
            "one, it becomes ninety, and the fifty pence never comes back. "
            "The screen says three hundred and eighty-two fifty. The email "
            "says three hundred and eighty-three pounds. [[slnc 350]] "
            "Nothing in the build objected. A customer sees one number at "
            "checkout and a different one in their inbox thirty seconds "
            "later, and there is no exception anywhere to explain why."
        ),
    ),
    dict(
        key="06-narrow-interface",
        kind="code",
        title="The Whole Mechanism, In One Interface",
        body="""public interface OrderSummaryView {

    String render(OrderSummaryModel model);
}
// one method. one parameter type.
// a view CANNOT be handed a price,
// a product, or a quantity to multiply.""",
        narration=(
            "So how does the pattern actually prevent this? Not with a "
            "warning, and not with a convention -- with an interface that "
            "is simply too narrow to allow the mistake. [[slnc 300]] Every "
            "view in this project implements one method, taking one "
            "parameter: a finished order summary model. That is it. There "
            "is no overload that accepts a product, or a price, or a "
            "quantity. [[slnc 350]] Read that narrowness as the actual "
            "enforcement mechanism, more than any rule written elsewhere. A "
            "view that wanted to compute its own total the honest way "
            "simply has nothing in its hand to compute one from -- which is "
            "exactly why the naive email view had to go around this "
            "interface entirely and import the product catalogue directly. "
            "That is not a coincidence. Going around the model is the only "
            "way the bug was ever going to be possible."
        ),
    ),
    dict(
        key="07-classic-vs-web",
        kind="quote",
        title="Classic MVC, And The MVC You Have Used",
        body=[
            "Classic: the view observes the model directly.",
            "",
            "Web MVC: the controller assembles a model once",
            "and hands it to a template. No observation at all.",
            "",
            "If you have used Spring, Rails or Django,",
            "you have already used the second one.",
        ],
        narration=(
            "I promised to be precise about which MVC we mean, so let's be "
            "precise. [[slnc 300]] Classic Smalltalk MVC has the view "
            "observe the model directly -- the model changes, and every "
            "subscribed view redraws itself without being told to, by "
            "name. [[slnc 350]] Web MVC -- the Spring, Rails or Django kind "
            "almost everyone meets first -- does not have this at all. A "
            "controller method assembles a model, often literally a map of "
            "key-value pairs, and hands it to a template engine, which "
            "renders once and is done. There is no ongoing subscription, "
            "because a web response is sent once and the page is gone. "
            "[[slnc 350]] If you have ever written a controller method that "
            "returns a view name and adds attributes to a model parameter, "
            "you have already used this half of the idea. You were simply "
            "never shown the Smalltalk half it is named after. This "
            "project's controller builds the model once and hands it "
            "directly to the views asked for, which is closer to the "
            "second kind -- and the notes explain exactly where the "
            "simplification sits."
        ),
    ),
    dict(
        key="08-mvp-mvvm",
        kind="bullets",
        title="MVP And MVVM, In One Scene",
        body=[
            "Same separation. Different arrows.",
            "",
            "MVP  --  the view is fully passive.",
            "         A Presenter pushes data into it.",
            "",
            "MVVM --  the view BINDS to a ViewModel.",
            "         A property change updates the",
            "         screen with no explicit push.",
        ],
        narration=(
            "Two more names get thrown around with MVC, and they deserve "
            "one scene each rather than being folded in as though they were "
            "the same thing. [[slnc 300]] MVP -- Model, View, Presenter -- "
            "makes the view fully passive. It has no reference to the model "
            "at all, and a presenter pulls data out and pushes it into the "
            "view through a small interface, which makes the view trivial "
            "to fake in a test. [[slnc 350]] MVVM -- Model, View, ViewModel "
            "-- goes one step further. The view binds to a view model's "
            "properties, so a property changing updates the screen with no "
            "explicit push at all. That is the mechanism most modern UI "
            "frameworks actually use under a different name -- data "
            "binding, reactive streams, whatever your framework calls it. "
            "[[slnc 300]] Properly teaching either one needs a real user "
            "interface toolkit with actual data binding, which a console "
            "demo does not have, so this video stops here. The distinction "
            "worth keeping: MVC's view can read its model directly, MVP's "
            "cannot, and MVVM's binds to it automatically."
        ),
    ),
    dict(
        key="09-rule-as-test",
        kind="code",
        title="The Rule, Written Where A Build Can Read It",
        body="""ArchRule rule = noClasses()
    .that().resideInAPackage(VIEW)
    .should().dependOnClassesThat()
        .resideInAPackage(INFRASTRUCTURE)
    .because(
        "a view that reads storage directly "
      + "can compute a number the model "
      + "never agreed to");

rule.check(layers);""",
        narration=(
            "So the narrow interface is the main defence, and this project "
            "also backs it with the same device the rest of the category "
            "uses. [[slnc 300]] No class in the view package may depend on "
            "classes in the infrastructure package. Read as English: a view "
            "is not allowed to reach into storage or the catalogue, which "
            "is precisely how the naive email view got the ingredients to "
            "compute a number of its own. [[slnc 350]] It runs in "
            "'gradlew test', alongside every other test, and it costs about "
            "thirty lines. And a second test widens that same rule to the "
            "naive package on purpose, and asserts that it fails, naming "
            "the rounded email view and the catalogue class it reached for."
        ),
    ),
    dict(
        key="10-red",
        kind="console",
        title="Watching It Go Red",
        body="""Architecture Violation [Priority: MEDIUM] -
  Rule 'no classes that reside in a package
  '..view..' should depend on classes that
  reside in a package '..infrastructure..''
  was violated (1 time):

Class <...naive.view.RoundedEmailView>
  depends on class
  <...infrastructure.ProductTable>""",
        narration=(
            "Here is what the build prints. Architecture violation. The "
            "rule was violated one time. [[slnc 300]] And then the part "
            "that matters: it names the class -- rounded email view -- and "
            "it names exactly what that class reached for -- the product "
            "table. [[slnc 350]] 'The email does not touch the catalogue' "
            "stopped being something a team promises at a whiteboard and "
            "forgets within a month, and became something that fails a "
            "build, by name, in under a second."
        ),
    ),
    dict(
        key="11-forced-change",
        kind="console",
        title="The Forced Change",
        body="""FORCED CHANGE: add a second view over the
  same model
  one screen  ->  one screen and one email,
  both reading the same OrderSummaryModel

  files added     : 1   EmailConfirmationView.java
  files modified  : 1   PlaceAnOrderDemo.java
  lines changed   : 2
  classes across model+controller+views : 21
  of those, opened                      : 1
  of those, never opened                : 20""",
        narration=(
            "So let's do it properly. The forced change this project "
            "performs: add a real second view, over the same model. [[slnc "
            "300]] Counted from the real files on disk: one file added, "
            "the new email view. One file modified -- the composition "
            "root, passing one extra argument. Two lines changed. [[slnc "
            "350]] Twenty-one classes make up the model, the controller and "
            "every view. Twenty of them were never opened. [[slnc 300]] But "
            "the number a file count alone cannot show you is the "
            "important one. The new view's total is not merely observed to "
            "match the screen's -- it is guaranteed to, because "
            "'EmailConfirmationView dot render' contains no arithmetic "
            "operator anywhere in it. It cannot compute a wrong answer. It "
            "cannot compute an answer at all."
        ),
    ),
    dict(
        key="12-agreement",
        kind="console",
        title="Both Views, Every Time",
        body="""FIVE. Add the real second view.
  Total: £382.50
  Thank you. Your order ord-1001 for
  £382.50 is confirmed.

  both views: £382.50. every time, because
  neither one is allowed to add up a price.""",
        narration=(
            "Run it, and here is act five in full. The screen says three "
            "hundred and eighty-two pounds fifty. The email says three "
            "hundred and eighty-two pounds fifty. [[slnc 300]] Not because "
            "somebody tested both and they happened to match today. Because "
            "there is exactly one place in this program that can produce an "
            "order total, and both renderers read it from there. Run it a "
            "thousand times with a thousand different orders, and the "
            "screen and the email will agree on every single one, for a "
            "reason stronger than testing can ever provide on its own: the "
            "email view is structurally incapable of disagreeing."
        ),
    ),
    dict(
        key="13-controllers-grow",
        kind="bullets",
        title="The Bill",
        body=[
            "A narrow interface is a real constraint.",
            "    A view that legitimately needs more has one",
            "    option: widen the model, for everyone.",
            "",
            "Controllers grow.",
            "    'Just one more check' is always easier to",
            "    add to the controller than to find a home for.",
        ],
        narration=(
            "Every project in this category has to pay a bill, honestly, "
            "and here is this one's. [[slnc 300]] A narrow view interface "
            "is a real constraint, not a free lunch. A view that "
            "legitimately needs something the model does not expose has "
            "exactly one honest option: widen the model, for every view, "
            "rather than reach around it. The architecture test only "
            "catches a view importing infrastructure -- it cannot catch a "
            "model quietly growing fifteen getters nobody else uses because "
            "one view once needed a sixteenth. [[slnc 350]] And the single "
            "most common failure of MVC in real production code: "
            "controllers grow. 'Just one more check' is always easier to "
            "add to the controller already handling the request than to "
            "find its proper home. This project's controller is three "
            "calls long, on purpose, and staying that short is a "
            "discipline the pattern does not enforce for you."
        ),
    ),
    dict(
        key="14-too-much",
        kind="bullets",
        title="When This Is Too Much",
        body=[
            "Worth it: more than one output has to represent",
            "the same state -- a screen and an email, a screen",
            "and a PDF receipt.",
            "",
            "Not worth it: exactly one output, that will",
            "never grow a second.",
        ],
        narration=(
            "So when is this not worth building? [[slnc 300]] A model, "
            "view and controller split earns its keep the moment more than "
            "one output has to represent the same underlying state -- a "
            "screen and an email, a screen and a PDF receipt, a desktop app "
            "and a command line. [[slnc 300]] It is not worth it for a "
            "program with exactly one output that is never going to grow a "
            "second. A single method that computes and prints in one pass, "
            "the way act one's naive screen did, is not a shortcut in that "
            "case. It is the whole of what is needed, and building three "
            "classes around it would be solving a problem that does not yet "
            "exist."
        ),
    ),
    dict(
        key="15-outro",
        kind="outro",
        title="Thanks for Watching",
        body=[
            "Full source, notes, diagrams and an animated walkthrough",
            "are in the repository. Try widening the model on purpose",
            "to fix the naive email properly, and watch both totals",
            "agree without a single line of arithmetic changing.",
        ],
        narration=(
            "That's MVC. [[slnc 250]] If you take one sentence away, take "
            "this one: two views cannot disagree about a number neither of "
            "them is allowed to calculate. [[slnc 350]] The full source, "
            "the written notes, the diagrams and an animated walkthrough "
            "are all in the repository, running offline with nothing "
            "installed but a Java development kit. [[slnc 300]] If you try "
            "one exercise, try this. Add a method to the model that exposes "
            "prices rounded to the nearest pound, properly, and rewrite the "
            "naive email to use it instead of reaching into the catalogue. "
            "Watch both totals agree -- not because you fixed the "
            "arithmetic, but because there is no longer any arithmetic in "
            "the view to get wrong. [[slnc 300]] If this helped, a like "
            "genuinely does help other people find it, and subscribe if "
            "you would like the rest of the series. [[slnc 250]] Thanks for "
            "watching, and I'll see you in the next one."
        ),
    ),
]
