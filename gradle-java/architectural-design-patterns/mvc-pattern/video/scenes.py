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
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Model View Controller pattern, in Java. [[slnc 300]] It is '
            'usually called M V C. [[slnc 300]] This video is presented '
            'by Jayasekhar Konduru. [[slnc 600]] First, a simple '
            'definition. [[slnc 300]] M V C splits a screen into three '
            'roles. [[slnc 400]] The model holds the data, and does the '
            'one calculation that matters. [[slnc 300]] The view turns '
            'that data into text, and calculates nothing. [[slnc 300]] '
            "And the controller takes the user's input, calls the model, "
            'and then asks a view to display the result. [[slnc 600]] '
            'Think of a newsroom. [[slnc 300]] The reporter writes the '
            'facts once. [[slnc 300]] The website and the printed paper '
            'both show the same facts. [[slnc 300]] Neither one is '
            'allowed to change the numbers. [[slnc 700]] In our online '
            'store, a screen and a confirmation email must both show the '
            'same order total. [[slnc 400]] In this video, we will see '
            'what happens when one of them works out the total for '
            'itself. [[slnc 300]] Why that is a structural bug, not a '
            'typo. [[slnc 300]] And which kind of M V C you have probably '
            'been using all along.'
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
            'Here is the job. [[slnc 300]] It is the same order as every '
            'project in this series. [[slnc 300]] A customer called Ada '
            'Okafor buys an espresso machine, a coffee grinder, and two '
            'bags of coffee beans, for three hundred and eighty-two '
            'pounds fifty. [[slnc 500]] The order has already been '
            'placed. [[slnc 300]] Now Ada must be told about it, twice. '
            '[[slnc 300]] Once in a summary on screen. [[slnc 300]] And '
            'once in a confirmation email, a moment later. [[slnc 500]] '
            'Both must say three hundred and eighty-two pounds fifty. '
            '[[slnc 300]] Remember that number, because for a while, one '
            'of them will not agree.'
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
            'We start with no separation at all. [[slnc 400]] One class '
            'checks the stock, takes the payment, and writes the screen '
            'text, all in one method. [[slnc 500]] It works. [[slnc 300]] '
            'And because there is only one calculation, the checkout and '
            'the screen text cannot disagree. [[slnc 500]] Its problem is '
            'different. [[slnc 300]] You cannot test whether the summary '
            'reads correctly, without running a whole checkout at the '
            'same time. [[slnc 300]] They are the same fourteen lines. '
            '[[slnc 500]] That is the cost of no separation. [[slnc 300]] '
            'But as we will hear shortly, the wrong kind of separation '
            'costs more.'
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
            'So here are the three roles, and what each one is not '
            "allowed to know. [[slnc 600]] The model holds the order's "
            'lines, and its one total. [[slnc 300]] It does not know how '
            'it will be shown: on a screen, in an email, or anywhere '
            'else. [[slnc 500]] The view turns the model into text. '
            '[[slnc 300]] It calculates nothing. [[slnc 300]] No adding, '
            'no rounding, no percentages. [[slnc 300]] If a view does '
            'arithmetic on a price, something has already gone wrong. '
            '[[slnc 500]] The controller places the order, and builds '
            'exactly one model from it. [[slnc 300]] Then it hands that '
            'same model to every view that needs it. [[slnc 600]] Here is '
            'the key sentence of this video. [[slnc 300]] Two views '
            'cannot disagree about a number that neither of them is '
            'allowed to calculate.'
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
            'Now for the moment this video is about. [[slnc 500]] The '
            'screen already works, reading the model. [[slnc 300]] Then '
            'someone is asked to write a confirmation email. [[slnc 300]] '
            'They want tidy prices, rounded to the nearest pound. [[slnc '
            '400]] The model has no method for that. [[slnc 300]] So '
            'instead of asking for one, the new email view reads the '
            'product catalogue directly. [[slnc 300]] And it rounds each '
            'price before multiplying. [[slnc 500]] It compiles. [[slnc '
            '300]] A reviewer sees a small, tidy view, and approves it. '
            '[[slnc 500]] But it prints a different total. [[slnc 300]] '
            'The coffee grinder costs eighty-nine pounds fifty. [[slnc '
            '300]] Rounded, it becomes ninety, and the fifty pence never '
            'comes back. [[slnc 500]] So the screen says three hundred '
            'and eighty-two pounds fifty. [[slnc 300]] And the email says '
            'three hundred and eighty-three pounds. [[slnc 500]] Nothing '
            'in the build objected. [[slnc 300]] The customer sees one '
            'number at checkout, and a different one in their inbox, '
            'thirty seconds later.'
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
            'So how does the pattern prevent this? [[slnc 400]] Not with '
            'a warning. [[slnc 300]] With an interface that is simply too '
            'narrow to allow the mistake. [[slnc 500]] Every view has '
            'exactly one method, called render. [[slnc 300]] It takes one '
            'thing: the finished order summary model. [[slnc 300]] There '
            'is no way to hand a view a product, a price, or a quantity. '
            '[[slnc 500]] So a view has nothing to calculate a total '
            'from. [[slnc 400]] That is exactly why the rounding email '
            'had to go around this interface, and read the catalogue '
            'directly. [[slnc 400]] Going around the model was the only '
            'way the bug could ever happen.'
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
            'Now, which M V C do we mean? [[slnc 300]] There are two main '
            'kinds. [[slnc 500]] The original, classic M V C comes from a '
            'language called Smalltalk. [[slnc 300]] There, the view '
            'watches the model. [[slnc 300]] When the model changes, '
            'every view redraws itself automatically. [[slnc 500]] Web M '
            'V C, the kind used by Spring, Rails and Django, works '
            'differently. [[slnc 300]] The controller builds a model '
            'once, and hands it to a template. [[slnc 300]] The template '
            'renders the page once, and it is done. [[slnc 300]] Nothing '
            'keeps watching. [[slnc 500]] If you have written a web '
            'controller that adds values to a model and returns a view '
            'name, you have used this second kind. [[slnc 400]] This '
            "project's controller builds the model once, and hands it to "
            'its views. [[slnc 300]] So it is closer to the web kind.'
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
            "Two related names often come up, so let's separate them. "
            '[[slnc 500]] M V P stands for Model, View, Presenter. [[slnc '
            '300]] Here the view is completely passive. [[slnc 300]] It '
            'never touches the model. [[slnc 300]] A presenter reads the '
            'data, and pushes it into the view. [[slnc 300]] That makes '
            'the view easy to fake in a test. [[slnc 500]] M V V M stands '
            'for Model, View, View Model. [[slnc 300]] Here the view is '
            "bound to the view model's properties. [[slnc 300]] When a "
            'property changes, the screen updates by itself, with no '
            'explicit push. [[slnc 300]] Many modern user interface '
            'frameworks work this way. [[slnc 500]] Teaching either one '
            'properly needs a real user interface toolkit, so this video '
            'stops here. [[slnc 400]] The short version. [[slnc 300]] In '
            'M V C, the view may read the model. [[slnc 300]] In M V P, '
            'it may not. [[slnc 300]] And in M V V M, it is bound to it '
            'automatically.'
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
            'The narrow interface is the main defence. [[slnc 300]] This '
            'project also adds a rule, written as a test with a library '
            'called ArchUnit. [[slnc 500]] No class in the view package '
            'may depend on any class in the infrastructure package. '
            '[[slnc 400]] In plain words, a view may not reach into '
            'storage or the catalogue. [[slnc 300]] That is exactly how '
            'the rounding email got the numbers to do its own sum. [[slnc '
            '500]] The test runs with every other test. [[slnc 300]] And '
            'a second test points the rule at the shortcut version, and '
            'expects it to fail.'
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
            'So what does a failure sound like? [[slnc 400]] The build '
            'reports an architecture violation, found once. [[slnc 300]] '
            'It names the class, Rounded Email View. [[slnc 300]] And it '
            'names what that class reached for, the Product Table. [[slnc '
            '500]] The promise that the email never touches the catalogue '
            'is no longer just a promise. [[slnc 300]] It fails the '
            'build, by name, in under a second.'
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
            "Now let's do it properly. [[slnc 300]] The change: add a "
            'real second view, the email, using the same model. [[slnc '
            '500]] Counted from the real files. [[slnc 300]] One file '
            'added: the new email view. [[slnc 300]] One file modified: '
            'the setup code, which passes one extra argument. [[slnc '
            '300]] Two lines changed. [[slnc 500]] The model, the '
            'controller and all the views make twenty-one classes. [[slnc '
            '300]] Twenty of them were never opened. [[slnc 500]] And '
            'here is the part a file count cannot show. [[slnc 300]] The '
            "new email's total is not just checked to match the screen. "
            '[[slnc 300]] It is guaranteed to, because the email view '
            'contains no arithmetic at all. [[slnc 300]] It cannot '
            'calculate a wrong answer, because it cannot calculate any '
            'answer.'
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
            "Let's run it. [[slnc 400]] The screen says three hundred and "
            'eighty-two pounds fifty. [[slnc 300]] The email says three '
            'hundred and eighty-two pounds fifty. [[slnc 500]] Not '
            'because someone tested both, and they happened to match '
            'today. [[slnc 300]] Because there is exactly one place in '
            'the program that can produce an order total. [[slnc 300]] '
            'And both views read it from there. [[slnc 500]] Run it with '
            'a thousand different orders, and they will agree every time. '
            '[[slnc 300]] The email view is simply unable to disagree.'
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
            "Every pattern has a cost, so let's name this one honestly. "
            '[[slnc 500]] First, a narrow view interface is a real limit. '
            '[[slnc 300]] If a view truly needs something the model does '
            'not offer, the honest fix is to widen the model, for every '
            'view. [[slnc 300]] Not to reach around it. [[slnc 300]] And '
            'no test will stop a model slowly growing methods that only '
            'one view ever uses. [[slnc 500]] Second, and most common: '
            'controllers grow. [[slnc 300]] Adding just one more check to '
            'the controller is always easier than finding the right home '
            "for it. [[slnc 400]] This project's controller is only three "
            'calls long, on purpose. [[slnc 300]] Keeping it short is a '
            'discipline the pattern does not enforce for you.'
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
            'So when is this not worth building? [[slnc 400]] M V C earns '
            'its keep when more than one output must show the same state. '
            '[[slnc 300]] A screen and an email. [[slnc 200]] A screen '
            'and a receipt. [[slnc 200]] A desktop app and a command '
            'line. [[slnc 500]] It is not worth it when there is exactly '
            'one output, and there will never be a second. [[slnc 300]] '
            'Then a single method that calculates and prints is not a '
            'shortcut. [[slnc 300]] It is all you need.'
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
            "That's M V C. [[slnc 400]] If you remember one sentence, "
            'make it this one. [[slnc 300]] Two views cannot disagree '
            'about a number that neither of them is allowed to calculate. '
            '[[slnc 500]] The full source code, written notes, diagrams, '
            'and an animated walkthrough are all in the repository. '
            '[[slnc 300]] It runs offline, with nothing installed except '
            'a Java development kit. [[slnc 500]] Here is one exercise to '
            'try. [[slnc 300]] Add a method to the model that gives '
            'prices rounded to the nearest pound. [[slnc 300]] Then '
            'change the shortcut email to use it, instead of reading the '
            'catalogue. [[slnc 300]] Both totals will agree, because '
            'there is no arithmetic left in the view to get wrong. [[slnc '
            '500]] If this helped, a like really does help other people '
            "find it. [[slnc 300]] And subscribe, if you'd like the rest "
            'of the series. [[slnc 400]] Thanks for watching.'
        ),
    ),
]
