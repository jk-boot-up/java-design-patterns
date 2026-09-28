"""Scene definitions for the Distributed Tracing teaching video.

Each scene has:
  key        - short id, used for the generated file names
  title      - slide heading
  kind       - "poster" | "bullets" | "code" | "console" | "quote" | "diagram" | "outro"
  body       - content, meaning depends on kind
  narration  - the text spoken by the narrator (see narration.md)

The narration is written to stand on its own. A large share of the audience
listens rather than watches -- on a phone, in a pocket, on a commute -- so no
sentence points at the screen, the analogy is spoken in full before any class
name, and the waterfall slides are described in words rather than left to the
picture. The slides illustrate the narration; they never carry it.

Every figure spoken aloud comes from the captured output of `./gradlew run`,
which is deterministic by construction: the clock is scripted, span ids are
sequential and the sampler counts rather than randomises. DemoRunsTest pins
the exact strings, so a change to the program that moved a number would fail
the build rather than quietly make this video wrong.

The running order mirrors the project. Scenes 2 to 4 are the problem, 5 to 11
are the pattern and its answer, and scenes 12 to 14 are the bill: a service
that opens no span, a context lost across a thread, and a trace thrown away
before anybody knew it mattered. None of the three raises an error, which is
why they get a third of the video rather than a footnote.
"""

SCENES = [
    # The poster is also the YouTube thumbnail, so it is the first frame of
    # the video and is saved separately as poster.png by build_video.sh.
    dict(
        key="01-poster",
        kind="poster",
        title="Distributed Tracing",
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Distributed Tracing pattern, in Java. [[slnc 300]] This '
            'video is presented by Jayasekhar Konduru. [[slnc 600]] '
            'First, a simple definition. [[slnc 300]] Distributed tracing '
            'gives one customer request a single I D. [[slnc 300]] Then '
            'every piece of work done for that request records two '
            'things. [[slnc 300]] How long it took. [[slnc 200]] And '
            'which piece of work asked for it. [[slnc 600]] Think of a '
            'hospital. [[slnc 300]] At reception you get a wristband with '
            'a number. [[slnc 300]] It follows you to X-ray, to the blood '
            "test, and to the doctor. [[slnc 300]] Each department's form "
            'carries your number, and says who sent you. [[slnc 300]] So '
            'afterwards, someone can rebuild your whole afternoon, in '
            'order. [[slnc 700]] In our online store, a product page '
            'takes nine hundred milliseconds. [[slnc 300]] Four healthy '
            'services helped build it, and nobody can say which one is '
            'slow. [[slnc 500]] By the end, you will know why merged logs '
            'cannot answer that. [[slnc 300]] The one subtraction that '
            'names the culprit. [[slnc 300]] And three ways this pattern '
            'quietly stops telling the truth.'
        ),
    ),
    dict(
        key="02-scenario",
        kind="bullets",
        title="The Scenario",
        body=[
            "An online shop. One customer opens one product page.",
            "",
            "    GET /product/A-2231        200 OK after 900ms",
            "",
            "Four services contributed to that page:",
            "",
            "    catalog            pricing",
            "    inventory          recommendations",
            "",
            "All four are healthy. All four are logging.",
            "Which one is slow?",
        ],
        narration=(
            'Here is the scenario. [[slnc 400]] A customer opens the page '
            'for one product. [[slnc 300]] It takes nine hundred '
            'milliseconds, slow enough to notice. [[slnc 500]] Four '
            'services helped build that page. [[slnc 300]] Catalog looked '
            'up the product. [[slnc 300]] Pricing worked out the price. '
            '[[slnc 300]] Inventory checked the stock. [[slnc 300]] And '
            'recommendations built a list of other things to buy. [[slnc '
            '600]] All four services are up. [[slnc 300]] All four are '
            'writing logs, and all the logs are correct. [[slnc 300]] '
            'Nothing is broken, and nothing is alerting. [[slnc 300]] But '
            'nobody can say which service spent the nine hundred '
            'milliseconds.'
        ),
    ),
    dict(
        key="03-problem",
        kind="console",
        title="What the Logs Give You",
        body="""  Every service logs. The aggregator merges the four logs by time.
  Two customers happen to be on the site at once.

  14:32:07.120  catalog          lookup complete
  14:32:07.120  pricing          quote started
  14:32:07.160  catalog          lookup complete
  14:32:07.160  pricing          quote started
  14:32:07.300  pricing          quote complete
  14:32:07.340  pricing          quote complete

  How long did pricing take?
  07.300 - 07.120 = 180ms?
  07.340 - 07.120 = 220ms?

  Four correct timestamps. No valid subtraction between any two.""",
        narration=(
            "So let's read the logs. [[slnc 400]] All four services write "
            'them, and a tool has merged them, in time order. [[slnc '
            '500]] Two customers happen to be on the site at the same '
            'moment. [[slnc 300]] That is normal. [[slnc 300]] So there '
            'are two lines saying pricing started a quote. [[slnc 300]] '
            'And two lines saying pricing finished one. [[slnc 600]] Now: '
            'how long did pricing take? [[slnc 500]] Match the first '
            'finish with the first start, and it is a hundred and eighty '
            'milliseconds. [[slnc 300]] Match the other finish, and it is '
            'two hundred and twenty. [[slnc 300]] Both look reasonable. '
            "[[slnc 300]] But one of them subtracts one customer's start "
            "from another customer's finish. [[slnc 500]] Every timestamp "
            'is correct. [[slnc 300]] And nothing tells you which lines '
            'belong together.'
        ),
    ),
    dict(
        key="04-not-detail",
        kind="bullets",
        title="More Logging Does Not Fix It",
        body=[
            "What would you add to those lines to make them answerable?",
            "",
            "    the thread name       fails the moment work crosses a thread",
            "    the pod name          same across both customers",
            "    the product id        both customers viewed A-2231",
            "    the response size     different, and meaningless",
            "",
            "The test each one fails:",
            "    the same across one request,",
            "    and different across the next.",
            "",
            "The missing thing is not detail. It is an identifier.",
        ],
        narration=(
            "The natural reaction is to log more. [[slnc 300]] So let's "
            'try it. [[slnc 500]] Add the thread name. [[slnc 300]] That '
            'fails as soon as the work moves to another thread. [[slnc '
            '400]] Add the machine name. [[slnc 300]] Both customers were '
            'served by the same machine. [[slnc 400]] Add the product. '
            '[[slnc 300]] Both customers viewed the same product. [[slnc '
            '600]] Every idea fails the same test. [[slnc 300]] You need '
            'something that is the same for everything done for one '
            'request. [[slnc 300]] And different for the next request. '
            '[[slnc 500]] So what is missing is not more detail. [[slnc '
            '300]] It is an I D.'
        ),
    ),
    dict(
        key="05-pattern",
        kind="quote",
        title="The Pattern",
        body=[
            "Give one request one identifier.",
            "",
            "Have every unit of work record",
            "how long it took —",
            "and what asked for it.",
            "",
            "Then the shape of the request",
            "is not designed. It is derived.",
        ],
        narration=(
            'Here is the pattern, in two parts. [[slnc 500]] First, give '
            'each customer request one I D, created at the front door. '
            '[[slnc 300]] Everything that happens because of that request '
            'carries it. [[slnc 300]] That is called the trace I D. '
            '[[slnc 600]] Second, every piece of work records four '
            'things. [[slnc 300]] What it was. [[slnc 200]] When it '
            'started. [[slnc 200]] How long it lasted. [[slnc 200]] And '
            'the I D of the piece of work that asked for it. [[slnc 500]] '
            'Each of those records is called a span. [[slnc 300]] And '
            'that last field is called the parent. [[slnc 600]] The first '
            'part lets you filter the logs down to one customer. [[slnc '
            '300]] The second part turns them into an answer. [[slnc '
            '300]] Because once every span knows its parent, the shape of '
            'the whole request can be rebuilt afterwards, by anyone.'
        ),
    ),
    dict(
        key="06-three-moves",
        kind="bullets",
        title="Three Moves",
        body=[
            "1.  Mint an id at the front door, and pass it on every call.",
            "",
            "        record TraceContext(String traceId, String spanId)",
            "",
            "2.  Open a span around each unit of work. Close it on the way out.",
            "",
            "        try (Tracer.Scope pricing = tracer.start(request, \"pricing\")) {",
            "",
            "3.  Start a nested span from the caller's context, not the page's.",
            "",
            "        tracer.start(recommendations.context(), \"ranking-model\")",
            "Move 3 is one argument. It is also the whole difference.",
        ],
        narration=(
            'In practice, that is three moves. [[slnc 500]] Move one. '
            '[[slnc 200]] The first service creates an I D, and passes it '
            'on with every call it makes. [[slnc 300]] It travels as two '
            'small values: the trace I D, and the I D of the span doing '
            'the calling. [[slnc 500]] Move two. [[slnc 200]] Each piece '
            'of work opens a span when it starts, and closes it when it '
            'finishes. [[slnc 300]] The span is only recorded when it '
            'closes, because only then is its length known. [[slnc 300]] '
            'A span that is never closed does not appear at all. [[slnc '
            '500]] Move three, the one people get wrong. [[slnc 200]] '
            'When one service calls another, the new span must be started '
            "from the caller's own span. [[slnc 300]] Not from the "
            "page's. [[slnc 300]] That one choice is the difference "
            'between a useful trace and a misleading one.'
        ),
    ),
    dict(
        key="07-roles",
        kind="diagram",
        title="Who Does What",
        body=None,
        narration=(
            "Let's name the pieces. [[slnc 300]] There are six, and they "
            'are all small. [[slnc 600]] A trace context: the two I Ds '
            'that travel with the request. [[slnc 300]] A span: one piece '
            'of work, with a name, a start, a length, and a parent. '
            '[[slnc 300]] A tracer: it hands out spans, and times them. '
            '[[slnc 500]] A trace: all the spans for one request. [[slnc '
            '300]] It does the arithmetic: which span is the first, which '
            'spans belong to which, and how much time each spent on its '
            'own work. [[slnc 500]] A drawing, which turns a trace into a '
            'picture. [[slnc 300]] The picture is built only from the '
            'parent field. [[slnc 500]] And the sixth piece is the merged '
            'log. [[slnc 300]] It is not part of the pattern. [[slnc '
            '300]] It is what the pattern replaces.'
        ),
    ),
    dict(
        key="08-the-parent",
        kind="code",
        title="The One Argument That Is the Pattern",
        body="""// inside ProductPage.load(traceId)

try (Tracer.Scope recommendations =
             tracer.start(request, "recommendations")) {

    try (Tracer.Scope model =
                 tracer.start(recommendations.context(), "ranking-model")) {
        clock.advance(RANKING_MODEL_MS);          // 340
    }
    clock.advance(RECOMMENDATIONS_MS - RANKING_MODEL_MS);   // 60
}

// pass `request` instead, and the arithmetic still closes.
// It is just no longer true.""",
        narration=(
            'Here is the one piece of code that matters, in words. [[slnc '
            '500]] The page opens a span called recommendations. [[slnc '
            "300]] It starts it from the page's own span. [[slnc 300]] So "
            'recommendations becomes a child of the page. [[slnc 600]] '
            'Inside it, a second span is opened, for the ranking model. '
            "[[slnc 300]] And this one is started from recommendations' "
            "span, not the page's. [[slnc 300]] So the ranking model is a "
            'child of recommendations, one level deeper. [[slnc 600]] Now '
            'here is the key point. [[slnc 300]] If you started it from '
            "the page's span by mistake, the program would still run. "
            '[[slnc 300]] The total would still be nine hundred '
            'milliseconds. [[slnc 300]] Everything would still add up. '
            '[[slnc 300]] And the answer would be wrong. [[slnc 500]] A '
            'trace can be perfectly consistent, and still false.'
        ),
    ),
    dict(
        key="09-parents",
        kind="console",
        title="Seven Spans, and the Column That Matters",
        body="""Act 3 - one id, and a parent for every piece of work

  catalog          span-2     parent span-1      120ms
  pricing          span-3     parent span-1      180ms
  inventory        span-4     parent span-1       90ms
  ranking-model    span-6     parent span-5      340ms
  recommendations  span-5     parent span-1      400ms
  render           span-7     parent span-1      110ms
  product-page     span-1     parent (none)      900ms

Six spans name a parent. One does not.
That one is the front door.""",
        narration=(
            "Let's run it. [[slnc 300]] One page load now produces seven "
            "spans. [[slnc 300]] Here is each span's parent. [[slnc 500]] "
            "Catalog's parent is span one, the page. [[slnc 300]] So are "
            'pricing, inventory, render, and recommendations. [[slnc '
            '500]] The ranking model is the odd one out. [[slnc 300]] Its '
            'parent is span five: recommendations. [[slnc 500]] And the '
            'page itself has no parent at all. [[slnc 300]] Exactly one '
            'span per request has no parent. [[slnc 300]] It is called '
            'the root. [[slnc 600]] This is still just a list. [[slnc '
            '300]] But it holds enough to rebuild the whole request, '
            'exactly as it happened.'
        ),
    ),
    dict(
        key="10-waterfall",
        kind="console",
        title="The Waterfall — That Column, Drawn",
        body="""Act 4 - the waterfall, which is the answer

  trace trace-4f2a   total 900ms
  product-page            |============================================|   900ms   0ms of it its own
    catalog               |=====                                       |   120ms
    pricing               |     ========                               |   180ms
    inventory             |              ====                          |    90ms
    recommendations       |                   ===================      |   400ms   60ms of it its own
      ranking-model       |                   ================         |   340ms
    render                |                                      ===== |   110ms

Nobody designed this shape. Nobody configured it.
Indentation is the parent field. Position is the start time.""",
        narration=(
            'Here are the same seven spans, drawn as a picture called a '
            "waterfall. [[slnc 300]] Let's describe it in words. [[slnc "
            '600]] The top line is the page. [[slnc 300]] Its bar runs '
            'the full nine hundred milliseconds. [[slnc 500]] One level '
            'below it, the bars appear in order, left to right. [[slnc '
            '300]] Catalog, a hundred and twenty milliseconds, right at '
            'the start. [[slnc 300]] Pricing, a hundred and eighty. '
            '[[slnc 300]] Inventory, ninety. [[slnc 300]] '
            'Recommendations, four hundred, by far the widest. [[slnc '
            '300]] And render, a hundred and ten, at the end. [[slnc '
            '500]] One level deeper, inside recommendations, sits the '
            'ranking model: three hundred and forty. [[slnc 600]] Nobody '
            'designed that shape. [[slnc 300]] The indenting comes from '
            'the parent field. [[slnc 300]] The position comes from the '
            'start time. [[slnc 300]] When a tracing tool shows a picture '
            'like this, it is showing your own data.'
        ),
    ),
    dict(
        key="11-self-time",
        kind="console",
        title="Self Time — The Whole Trick",
        body="""  Time by service, excluding what each was waiting on:

    ranking-model     340ms   37% of the page
    pricing           180ms   20% of the page
    catalog           120ms   13% of the page
    render            110ms   12% of the page
    inventory          90ms   10% of the page
    recommendations    60ms    6% of the page

  The page lasted 900ms and did 0ms of its own work.

  340 + 180 + 120 + 110 + 90 + 60  =  900ms""",
        narration=(
            'Now the arithmetic. [[slnc 300]] It is one subtraction, and '
            "it is the whole trick. [[slnc 600]] A span's length is how "
            'long it lasted. [[slnc 300]] Its self time is its length, '
            'minus the length of its children. [[slnc 300]] In other '
            'words, the time it was working, not waiting. [[slnc 600]] '
            'Apply that to the page. [[slnc 300]] It lasted the full nine '
            'hundred milliseconds, so it always looks biggest. [[slnc '
            '300]] But its self time is zero. [[slnc 300]] It did '
            'nothing. [[slnc 300]] It waited. [[slnc 500]] Think of a '
            "manager whose whole day was spent in other people's "
            'meetings. [[slnc 300]] The longest day on the team, and no '
            'work of their own. [[slnc 600]] Recommendations lasted four '
            'hundred milliseconds. [[slnc 300]] But only sixty were its '
            'own. [[slnc 300]] The other three hundred and forty belong '
            'to the ranking model. [[slnc 500]] So the ranking model is '
            'the top of the list. [[slnc 300]] Three hundred and forty '
            "milliseconds, thirty-seven percent of the customer's wait. "
            '[[slnc 500]] The question from the start is answered, by '
            'subtraction, afterwards.'
        ),
    ),
    dict(
        key="12-uninstrumented",
        kind="console",
        title="The Bill, Part One — A Service That Opens No Span",
        body="""Act 5 - recommendations never opens a span. It still forwards
        the context faithfully. Nothing errors. Nothing warns.

  trace trace-7c19   total 900ms
  product-page            |============================================|   900ms   60ms of it its own
    catalog               |=====                                       |   120ms
    pricing               |     ========                               |   180ms
    inventory             |              ====                          |    90ms
    ranking-model         |                   ================         |   340ms
    render                |                                      ===== |   110ms

  one root.  no orphans.  900ms fully accounted for.
  and the service responsible is not on the diagram at all.""",
        narration=(
            'That is the pattern, and it works. [[slnc 300]] Now the '
            'bill, with three items. [[slnc 600]] Item one: a service '
            'that opens no span. [[slnc 300]] Recommendations never '
            'records a span of its own. [[slnc 300]] But it still passes '
            'the trace I D on to the ranking model. [[slnc 300]] So '
            'nothing fails, and nothing warns. [[slnc 600]] Listen to '
            'what happens. [[slnc 300]] Now there are six spans, not '
            'seven. [[slnc 300]] The ranking model appears directly under '
            'the page, as if the page called it. [[slnc 300]] Nothing in '
            'the code does that. [[slnc 500]] And sixty milliseconds land '
            'on the page. [[slnc 300]] So the page now seems to do sixty '
            'milliseconds of its own work. [[slnc 300]] It does none. '
            '[[slnc 600]] By every check you might run, this trace looks '
            'healthy. [[slnc 300]] But the service really responsible is '
            'missing. [[slnc 300]] And someone spends the afternoon '
            'investigating the page instead. [[slnc 500]] That is why '
            'partial tracing is worse than none. [[slnc 300]] None tells '
            'you nothing. [[slnc 300]] Partial tells you something false, '
            'with confidence.'
        ),
    ),
    dict(
        key="13-thread",
        kind="console",
        title="The Bill, Part Two — One Line, in the Wrong Place",
        body="""Act 6 - the context lives in a ThreadLocal.
        The work moves to a worker thread.

  trace trace-async-broken   total 400ms   2 separate roots - this trace is broken
  product-page            |============================================|   400ms
  recommendations         |============================================|   400ms

  no exception.  no warning.  400ms belonging to nobody.

  the fix - read the context on the thread that has it:

  trace trace-async-fixed   total 400ms
  product-page            |============================================|   400ms   0ms of it its own
    recommendations       |============================================|   400ms""",
        narration=(
            'Item two: one line in the wrong place. [[slnc 500]] The '
            'recommendations call is moved onto a separate worker thread. '
            '[[slnc 300]] So the page can do other things while it runs. '
            '[[slnc 300]] A sensible change. [[slnc 600]] But the trace I '
            'D is kept in a variable that belongs to one thread only. '
            "[[slnc 300]] The page's thread has it. [[slnc 300]] The "
            "worker thread never did. [[slnc 300]] So the worker's span "
            'has no parent. [[slnc 600]] Now there are two roots in one '
            'trace. [[slnc 300]] The page, and recommendations, side by '
            'side. [[slnc 300]] Four hundred milliseconds of work that '
            'belong to nobody. [[slnc 300]] No error. [[slnc 300]] No '
            'warning. [[slnc 600]] The fix is to move one line earlier. '
            '[[slnc 300]] Read the trace I D on the thread that has it. '
            '[[slnc 300]] And hand it to the worker as an ordinary value. '
            '[[slnc 500]] Now there is one root, with recommendations '
            'under it, where it belongs. [[slnc 300]] The broken and '
            'working versions differ by one line, in a different place.'
        ),
    ),
    dict(
        key="14-sampling",
        kind="console",
        title="The Bill, Part Three — The Decision Made Too Early",
        body="""Act 7 - a million requests today. The front door keeps one
        trace in a hundred.

  kept       10,000
  discarded  990,000

  A customer complains about request number 862,144.
  Was it kept?  no - it is gone, and it is not recoverable

  The decision was made at the front door, before anybody
  knew the request was going to matter.

  The way out: tail sampling. Hold the spans. Decide at the end.""",
        narration=(
            'Item three: a decision made too early. [[slnc 500]] Storing '
            'every span is expensive. [[slnc 300]] So the front door '
            'keeps only one trace in every hundred. [[slnc 300]] And '
            'throws the rest away. [[slnc 600]] Out of a million requests '
            'today, ten thousand traces are kept. [[slnc 300]] Nine '
            'hundred and ninety thousand are gone. [[slnc 500]] Then a '
            'customer complains about one particular slow page. [[slnc '
            '300]] Its trace was not kept. [[slnc 300]] It is gone for '
            'good. [[slnc 300]] It was thrown away at the front door, '
            'before anyone knew it would be slow. [[slnc 600]] So a one '
            'percent sample can tell you recommendations is slow on '
            'average. [[slnc 300]] But it cannot tell you why this one '
            'request was slow. [[slnc 600]] The way out is called tail '
            'sampling. [[slnc 300]] Hold the spans briefly, let the '
            'request finish, and then keep the trace if it was slow, or '
            'if it failed. [[slnc 300]] The decision moves to the end, '
            'the only place it can be made well.'
        ),
    ),
    dict(
        key="15-boundary",
        kind="bullets",
        title="What to Take Away",
        body=[
            "A trace id makes a log readable.",
            "A parent span id makes it an answer.",
            "Do both, or the second half of the value never arrives.",
            "",
            "Self time, not total time.",
            "The longest span is always the request, and always innocent.",
            "",
            "The context dies at boundaries.",
            "Threads, queues, scheduled jobs. Pass it as a value.",
            "",
            "Logs, metrics and traces answer three different questions.",
            "Most teams try to make logs answer all three.",
        ],
        narration=(
            'Here are three things to remember. [[slnc 500]] One. [[slnc '
            '200]] A trace I D makes the logs readable. [[slnc 300]] A '
            'parent I D turns them into an answer. [[slnc 400]] Two. '
            '[[slnc 200]] Look at self time, not total time. [[slnc 300]] '
            'The longest span is always the request itself, and it is '
            'always innocent. [[slnc 400]] Three. [[slnc 200]] The trace '
            'I D gets lost at boundaries: threads, queues, and scheduled '
            'jobs. [[slnc 300]] Pass it as an ordinary value. [[slnc '
            '600]] And one boundary worth knowing. [[slnc 300]] Tracing '
            'is one of three tools, with logs and metrics. [[slnc 300]] '
            'Logs answer: what was the error? [[slnc 300]] Metrics '
            'answer: how does today compare with yesterday? [[slnc 300]] '
            'Traces answer: where did the time go, in this one request? '
            '[[slnc 500]] Many teams try to make logs do all three. '
            '[[slnc 300]] That is exactly where this video started: four '
            'correct logs, and no answer.'
        ),
    ),
    dict(
        key="16-outro",
        kind="outro",
        title="Thanks for Watching",
        body=[
            "Full source, tests, diagrams and an interactive animation",
            "are in the repository — including both sides of every failure.",
            "",
            "Run it yourself:  ./gradlew run",
        ],
        narration=(
            "That's the Distributed Tracing pattern. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] One I '
            'D for the request, one parent for every piece of work, and a '
            'subtraction that turns them into an answer. [[slnc 500]] The '
            'full source code, written notes, diagrams, and an animated '
            'walkthrough are all in the repository. [[slnc 300]] It runs '
            'offline, with nothing installed except a Java development '
            'kit. [[slnc 300]] Both the broken and the working version of '
            'every failure are there to run. [[slnc 500]] Here is one '
            'exercise to try. [[slnc 300]] Find one place in your own '
            'code where work is handed to another thread. [[slnc 300]] '
            'And check whether the trace I D makes the trip. [[slnc 500]] '
            'If this helped, a like really does help other people find '
            "it. [[slnc 300]] And subscribe, if you'd like the rest of "
            'the series. [[slnc 400]] Thanks for watching.'
        ),
    ),
]
