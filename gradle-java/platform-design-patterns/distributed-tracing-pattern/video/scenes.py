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
            "Hello, and welcome. This video explains the Distributed Tracing "
            "design pattern in Java, and it is written and presented by "
            "Jayasekhar Konduru. [[slnc 300]] Let's start with the simple "
            "definition. Distributed tracing means giving one customer request a "
            "single identifier, and then having every piece of work done for that "
            "request record two things: how long it took, and which piece of work "
            "asked for it. [[slnc 350]] Think of a hospital. You arrive at "
            "reception and you are given a wristband, and that wristband follows "
            "you to X-ray, to the blood test, to the consultant. Every department "
            "writes on their own form, but every form carries your number, so "
            "afterwards somebody can put your whole afternoon back together in "
            "order. [[slnc 300]] And notice the second half. Each form also says "
            "who sent you — reception sent you to X-ray, X-ray sent you for "
            "bloods. That is the bit that turns a pile of forms into a story. "
            "[[slnc 350]] That's the idea in a sentence. The rest of the video "
            "does it properly, by building a real working Java project: an online "
            "shop with a product page that takes nine hundred milliseconds, four "
            "healthy services that all contributed to it, and nobody able to say "
            "which one is at fault. [[slnc 250]] By the end you'll know why "
            "merged logs cannot answer that question no matter how much you add "
            "to them, the one piece of arithmetic that names the culprit, and the "
            "three ways this pattern quietly stops telling you the truth without "
            "ever raising an error."
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
            "So, imagine an online shop. A customer opens the page for one "
            "product, and the page takes nine hundred milliseconds to come back. "
            "That is slow enough to feel. [[slnc 300]] Four services contributed "
            "to that page. Catalog looked the product up. Pricing worked out what "
            "to charge. Inventory checked there was stock. And recommendations "
            "built the strip of other things the customer might like. [[slnc "
            "300]] Now here is the situation, and it is worth sitting with for a "
            "moment. All four of those services are up. All four are responding. "
            "All four are writing logs, and all of those logs are correct. "
            "Nothing is broken, nothing is alerting, and nobody in the building "
            "can tell you which of the four spent the nine hundred milliseconds. "
            "[[slnc 350]] There is exactly one measurement in this picture, and "
            "it is the complaint."
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
            "So let's do the obvious thing and go and read the logs. Every "
            "service writes them, and an aggregator has merged all four together "
            "in time order. [[slnc 300]] Two customers happen to be on the site "
            "at the same moment, which is not a coincidence you have to arrange — "
            "it is a Tuesday. So there are two lines saying pricing started a "
            "quote, and two lines saying pricing finished one. [[slnc 350]] Now "
            "answer the question. How long did pricing take? [[slnc 400]] Take "
            "the first finish away from the first start and the answer is a "
            "hundred and eighty milliseconds. Take the second finish instead and "
            "the answer is two hundred and twenty. Both of those look entirely "
            "reasonable, and one of them is one customer's start subtracted from "
            "another customer's finish. [[slnc 350]] Every one of those four "
            "timestamps is correct. There is no valid subtraction between any two "
            "of them, and nothing on any line tells you which pairs with which."
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
            "The instinct at this point is to log harder. So let's take that "
            "seriously and try it. [[slnc 300]] Add the thread name. That works "
            "right up until the work moves onto another thread, which it will, "
            "and which is going to come back and bite us later in this video. "
            "[[slnc 250]] Add the name of the machine or the pod. Both customers "
            "were served by the same one, so that tells you nothing. Add the "
            "product id. Both customers were looking at the same product. Add the "
            "size of the response — different for each, and completely "
            "meaningless. [[slnc 350]] Every suggestion fails the same test, and "
            "the test is worth saying slowly. You need something that is the same "
            "across everything done for one request, and different for the next "
            "request. [[slnc 300]] None of those fields is that. So the missing "
            "thing is not more detail. It is an identifier."
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
            "Here, then, is the pattern, and it is two sentences. [[slnc 300]] "
            "Give one customer request one identifier, minted at the front door "
            "and carried by everything that happens because of it. That is called "
            "the trace id. [[slnc 350]] Then have every individual unit of work "
            "record four things: what it was, when it started, how long it "
            "lasted, and — this is the one that matters — the identifier of the "
            "unit of work that asked for it. One of those records is called a "
            "span, and that last field is called the parent span id. [[slnc "
            "400]] The first sentence makes the logs readable, because you can "
            "filter them down to one customer. The second sentence is what makes "
            "them an answer. [[slnc 300]] Because once every span knows what "
            "caused it, the shape of the request is not something anybody has to "
            "design or draw. It is already in the data, and it can be worked out "
            "afterwards by anybody, with no cooperation from the services that "
            "produced it."
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
            "In practice that is three moves. [[slnc 300]] Move one. The first "
            "service to see the request makes up an identifier and passes it on "
            "with every call it makes. In this project that travels as a little "
            "value holding two strings: the trace id, and the id of the span "
            "doing the calling. Two strings. Everything else is bookkeeping. "
            "[[slnc 350]] Move two. Each unit of work opens a span when it starts "
            "and closes it when it finishes. The closing is load-bearing, because "
            "the duration is not known until the work is over, so the span is "
            "only recorded on the way out. A span that is opened and never closed "
            "does not appear at all. [[slnc 350]] Move three, and this is the one "
            "people get wrong. When one service calls another, the nested span "
            "must be started from the calling service's own context, not from the "
            "page's. [[slnc 250]] That is one argument in one method call, and it "
            "is the entire difference between a useful trace and a misleading "
            "one. We will see exactly why in a few minutes."
        ),
    ),
    dict(
        key="07-roles",
        kind="diagram",
        title="Who Does What",
        body=None,
        narration=(
            "Let me name the pieces, because there are only six of them and they "
            "are all small. [[slnc 300]] A trace context is two strings that "
            "travel with the request. A span is one recorded unit of work: a "
            "name, a start, a duration, and the id of its parent. A tracer hands "
            "out spans and times them against a clock. [[slnc 350]] A trace is "
            "the whole collection of spans for one request, and it is where the "
            "arithmetic lives — which span is the root, which spans are whose "
            "children, and how much time each span spent on its own work. [[slnc "
            "300]] Then there is the drawing, which reads a trace and produces "
            "text, and which the trace has never heard of. That one-way "
            "relationship is worth noticing. There is no layout object anywhere "
            "in this project and no notion of a view. The picture is a rendering "
            "of the parent field and nothing else. [[slnc 350]] And the sixth "
            "piece is the merged log, which is connected to nothing at all, "
            "because it is not part of the pattern. It is the thing the pattern "
            "replaces."
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
            "This is the one piece of code worth reading closely, and I will "
            "describe it rather than spell out the syntax. [[slnc 300]] The page "
            "opens a span called recommendations, and it starts that span from the "
            "page's own context — so recommendations becomes the page's child. "
            "Correct. [[slnc 350]] Then, inside it, a second span is opened for "
            "the ranking model. And the context handed to that second call is not "
            "the page's. It is recommendations' own context, taken from the scope "
            "that was just opened. So the model becomes recommendations' child, "
            "and sits one level deeper. [[slnc 400]] Now here is the thing to "
            "hold onto. If you passed the page's context there instead, the "
            "program would still run. The total would still be nine hundred "
            "milliseconds. Every number would still add up. The trace would still "
            "have exactly one root and no orphans. [[slnc 300]] And the answer it "
            "gave you would be wrong. A trace can be completely self-consistent "
            "and false, and that idea is the most useful thing in this video."
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
            "So let's run it. One page load now produces seven spans, and I am "
            "going to read you the parent column, because that column is the "
            "pattern. [[slnc 300]] Catalog says its parent is span one. Pricing "
            "says span one. Inventory says span one. Render says span one. "
            "Recommendations says span one. [[slnc 250]] The ranking model is the "
            "odd one out: its parent is span five, which is recommendations. "
            "[[slnc 350]] And the last line, the product page itself, has no "
            "parent at all. Exactly one span per request has no parent, and that "
            "is the front door. It is called the root. [[slnc 300]] Now, nothing "
            "here is a picture yet. This is a flat list, and the order it came "
            "out in is not even the order things happened. But that column has "
            "enough in it to rebuild the request exactly as it was, and that is "
            "what happens next."
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
            "Here is the same seven spans, drawn. And because a picture is no use "
            "to you if you are listening rather than watching, let me describe it "
            "properly. [[slnc 300]] The top line is the page, and its bar runs "
            "the full width, because it is the whole nine hundred milliseconds. "
            "[[slnc 250]] Indented one level under it, four bars sit side by "
            "side, left to right, in the order they happened: catalog for a "
            "hundred and twenty milliseconds at the very start, pricing for a "
            "hundred and eighty, inventory for ninety, and then recommendations "
            "for four hundred, which is by far the widest of the four. Finally "
            "render, a hundred and ten, tucked against the right-hand edge. "
            "[[slnc 350]] And indented one level deeper again, inside "
            "recommendations, sits the ranking model at three hundred and forty. "
            "[[slnc 350]] Now the important part. Nobody designed that shape. "
            "Nobody configured it. The indentation is the parent field, and the "
            "position of each bar is its start time. That is all. When you open a "
            "hosted tracing tool and see a picture like this, you are not looking "
            "at something the tool invented. You are looking at your own data."
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
            "And now the arithmetic, which is one subtraction and is the whole "
            "trick. [[slnc 300]] A span's duration is how long it lasted. Its "
            "self time is its duration minus however long its children lasted — "
            "in other words, the time it was actually working rather than "
            "waiting. [[slnc 350]] Apply that to the page. It lasted the full "
            "nine hundred milliseconds, so on total time it is the biggest thing "
            "in the trace, and it always will be, in every trace you ever look "
            "at. Its self time is zero. It did nothing. It waited. [[slnc 400]] "
            "If that feels slippery, think of a manager whose day is eight hours "
            "long and who spent all eight of them in meetings run by other "
            "people. Their day is the longest on the team. Their own work is "
            "zero. [[slnc 350]] Recommendations lasted four hundred milliseconds "
            "and is charged only sixty, because three hundred and forty of them "
            "belong to the model it called. And the top of the ranking is the "
            "ranking model itself, at three hundred and forty milliseconds — "
            "thirty-seven per cent of what the customer waited for. [[slnc 300]] "
            "That is the question from the start of this video, answered. And "
            "notice when it was answered: afterwards, by subtraction, from data "
            "nobody had to know in advance they would need."
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
            "So that is the pattern, and it works. Now the bill, because there "
            "are three items on it, and all three are the price of the pattern "
            "rather than mistakes made while applying it. [[slnc 350]] Item one. "
            "Recommendations is a well-behaved service in every respect but one: "
            "it never opens a span of its own. It still receives the trace "
            "context and still forwards it faithfully to the ranking model. So "
            "nothing errors and nothing warns. [[slnc 350]] Listen to what "
            "happens to the shape. There are now six spans instead of seven, and "
            "the ranking model has moved up a level: it is indented directly "
            "under the page, as though the page called it, which nothing in the "
            "code does. [[slnc 300]] And the four hundred milliseconds did not "
            "disappear. Sixty of them landed on the parent, so the page now "
            "appears to do sixty milliseconds of its own work. It does none. "
            "[[slnc 400]] Now check this trace the way you would check any trace. "
            "It has one root. It has no orphans. Every millisecond is accounted "
            "for. By every test you would think to run, it is healthy — and the "
            "service actually responsible is not on the diagram at all. Somebody "
            "spends the afternoon reading the page renderer. [[slnc 300]] That is "
            "why partial instrumentation is worse than none. None tells you "
            "nothing. Partial tells you something false, confidently, with a "
            "diagram."
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
            "Item two, and this is the one that catches everybody. [[slnc 300]] "
            "The recommendations call is moved onto a worker thread, so the page "
            "can get on with other things while it runs. Perfectly sensible "
            "change. [[slnc 300]] But the trace context is being kept in a "
            "thread-local — a variable whose value is private to each thread. The "
            "page's thread has one. The worker thread has never had one. So the "
            "worker asks for the context and is handed nothing, and it opens its "
            "span with no parent. [[slnc 350]] The result is two roots in one "
            "trace: the page on one line, and recommendations on another, both "
            "four hundred milliseconds, neither one inside the other. Four "
            "hundred milliseconds of work belonging to nobody. No exception. No "
            "warning. [[slnc 400]] And the fix is one line, moved earlier. Read "
            "the context on the thread that actually has it, and hand it to the "
            "task as an ordinary value, because a value does not care which "
            "thread reads it. [[slnc 300]] Same two spans, same four hundred "
            "milliseconds, and now one root with recommendations indented "
            "underneath it where it belongs. The broken version and the working "
            "version are the same code with one line in a different place. "
            "[[slnc 250]] So here is something to do this week. Find one place in "
            "your own codebase where work is handed to an executor or a future, "
            "and check whether anything traced happens inside it."
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
            "Item three, and this one is about money. [[slnc 300]] A thousand "
            "requests a second, at six spans each, is roughly half a billion "
            "spans a day. Nobody pays to store that, so the front door keeps one "
            "trace in a hundred and throws the rest away. [[slnc 350]] A million "
            "requests today leaves ten thousand traces kept and nine hundred and "
            "ninety thousand gone. And then a customer complains about one "
            "specific page load — request number eight hundred and sixty-two "
            "thousand, one hundred and forty-four. [[slnc 300]] It was not kept. "
            "It is gone, and it is not recoverable, and it was thrown away at the "
            "front door, at the only moment in the whole request when nothing "
            "whatsoever was known about it. [[slnc 400]] That is the honest "
            "trade. A one per cent sample answers 'recommendations is slow on "
            "average' perfectly well, and cannot answer 'why was this one slow' "
            "at all. [[slnc 300]] The way out is called tail sampling. Hold the "
            "spans in memory, let the request finish, and then decide to keep the "
            "trace if it was slow or if it failed. The decision moves from the "
            "front door to after the fact, which is the only place it can be made "
            "well."
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
            "Three things to take away, and then one boundary worth drawing. "
            "[[slnc 300]] First: a trace id makes a log readable, and a parent "
            "span id makes it an answer. If you only do the first, you get "
            "filtering, which is genuinely useful and is not this pattern. "
            "[[slnc 300]] Second: self time, not total time. The longest span in "
            "any trace is the request itself, and it is always innocent. [[slnc "
            "300]] Third: the context dies at boundaries — threads, queues, "
            "scheduled jobs, anything asynchronous. Pass it as an ordinary value "
            "and never trust a thread-local to make the trip. [[slnc 350]] And "
            "the boundary. Tracing is one of three things, alongside logs and "
            "metrics, and they answer three different questions. Logs answer "
            "'what was the error message'. Metrics answer 'how does today compare "
            "with yesterday'. Traces answer 'where did the time go in this one "
            "request'. [[slnc 300]] Most teams try to make logs do all three, "
            "which is exactly the situation we started this video in — four "
            "correct logs and no answer."
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
            "And that is distributed tracing. One identifier for the request, one "
            "parent for every piece of work, and a subtraction that turns the "
            "result into an answer. [[slnc 350]] The whole project is in the "
            "repository — the source, eighty-two tests, the diagrams, and an "
            "interactive animation that builds the waterfall up one span at a "
            "time. Both sides of every failure are in there too, so you can run "
            "the broken version and the working one and compare them yourself. "
            "[[slnc 300]] If this was useful, please like the video and "
            "subscribe. Thanks very much for watching, and I'll see you in the "
            "next one."
        ),
    ),
]
