"""Scene definitions for the Distributed Tracing with Jaeger teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks every count out loud, says each of the tools' words in plain
language before using the tool's name for it, and never points at a picture
the listener cannot see. Every figure is the output of `./gradlew run`.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Distributed Tracing with Jaeger',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Distributed Tracing pattern in Java, using a real tracing '
            'library called OpenTelemetry, and a real trace collector '
            'called Jaeger. [[slnc 300]] This video is presented by '
            'Jayasekhar Konduru. [[slnc 600]] First, a simple definition. '
            '[[slnc 300]] Distributed tracing gives one customer request one '
            'identifier. [[slnc 300]] Every piece of work records how long '
            'it took, and which piece of work asked for it. [[slnc 300]] '
            'Afterwards, those records are put back together into one '
            'story. [[slnc 700]] Think of a hospital. [[slnc 300]] At '
            'reception you get a wristband with a number on it. [[slnc 300]] '
            'X-ray, the blood test and the consultant each write their own '
            'form, with your wristband number on it. [[slnc 300]] At the end '
            'of the shift, the records office puts your afternoon back '
            'together, by that number. [[slnc 700]] In our online store, one '
            'product page is built by two programs. [[slnc 300]] By the end, '
            'you will hear a page split into two stories because one header '
            'was forgotten. [[slnc 300]] A trace that arrives late, or not at '
            'all. [[slnc 300]] A customer complaint with no trace to look at. '
            '[[slnc 300]] And a clock that makes an answer arrive before its '
            'question.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['The product page: catalog, pricing,', 'inventory, then a call to', 'recommendations, then render.', '',
              'Recommendations: a second Java', 'program, with a slow ranking model.', '',
              'Both are real HTTP servers.', 'Jaeger runs in a container.'],
        narration=(
            'Here is the scenario. [[slnc 400]] The product page is the '
            'front door. [[slnc 300]] It looks the product up in the '
            'catalog, asks pricing for a price, and checks the stock. [[slnc '
            '300]] Then it calls a second program, the recommendations '
            'service, over the network. [[slnc 300]] And then it builds the '
            'page. [[slnc 600]] Recommendations runs a ranking model, the '
            'slowest single piece of work on the page. [[slnc 600]] Both are '
            'real web servers, in two separate Java programs. [[slnc 300]] '
            'And the collector, Jaeger, runs in a container that the demo '
            'starts by itself. [[slnc 300]] The plain Java version of this '
            'video kept everything inside one program. [[slnc 300]] Here, '
            'nothing is shared except the network.'
        ),
    ),
    dict(
        key='03-words', kind='bullets', title="The Tools' Words",
        body=['A span: one piece of work,', 'with its length and its parent.', '',
              'The trace ID: the wristband number.', '',
              'traceparent: the header that carries it,', '55 characters.', '',
              'Jaeger: the records office.'],
        narration=(
            'These tools bring a few words with them. [[slnc 400]] One form, '
            'for one piece of work, is called a span. [[slnc 300]] It has a '
            'name, a start time, a length, and the ID of the span that asked '
            'for it, called its parent. [[slnc 300]] A span with no parent '
            'is the front door, and is called the root. [[slnc 600]] The '
            'wristband number is called the trace ID. [[slnc 300]] Every '
            'span of one customer request carries the same one. [[slnc 600]] '
            'The wristband travels from one program to the next in a web '
            'header, called trace parent. [[slnc 300]] It is fifty-five '
            'characters long. [[slnc 300]] Writing it onto an outgoing '
            'request is called injecting. [[slnc 300]] Reading it from an '
            'incoming one is called extracting. [[slnc 600]] And Jaeger is '
            'the records office. [[slnc 300]] It receives every '
            "service's spans, and joins them by trace ID."
        ),
    ),
    dict(
        key='04-one', kind='console', title='A Hop That Forgets The Header',
        body="""ONE. A hop that forgets the header.
  the page calls recommendations
  over real HTTP.
  traceparent sent: none.

  Jaeger holds 2 traces for one page load.
  trace 1: 6 spans, all from product-page.
    its call to recommendations: 0 spans under it.
  trace 2: 2 spans, all from recommendations.
    the ranking model, with no page above it.""",
        narration=(
            'First demo: a hop that forgets the header. [[slnc 400]] The '
            'product page calls recommendations over the network. [[slnc '
            '300]] But it leaves out the one line that writes the trace '
            'parent header. [[slnc 600]] Nothing fails. [[slnc 300]] '
            'Recommendations finds no header, so it starts a story of its '
            'own. [[slnc 600]] Jaeger now holds two traces, for one page '
            "load. [[slnc 300]] The page's trace has six spans. [[slnc 300]] "
            'Its call to recommendations has nothing under it. [[slnc 300]] '
            'The other trace has two spans: recommendations, and its ranking '
            'model, with no page above them. [[slnc 600]] And each trace '
            'looks perfectly healthy. [[slnc 300]] The two halves could only '
            'be found together by searching both services for a visit number '
            'the shop happened to record.'
        ),
    ),
    dict(
        key='05-two', kind='console', title='The Header Forwarded',
        body="""TWO. The header forwarded.
  one line added: inject the current context.
  sent:     00-bfc846...532f-b9f24f7bae4a6586-01
  received: 00-bfc846...532f-b9f24f7bae4a6586-01

  Jaeger holds 1 trace:
  8 spans from 2 services, 1 root.
  slowest by its own time:
  ranking-model, 340 ms or more.""",
        narration=(
            'Second demo: the header forwarded. [[slnc 400]] One line is '
            'added. [[slnc 300]] Write the current trace onto the outgoing '
            'request. [[slnc 600]] The header the page sent, and the header '
            'recommendations received, are the same fifty-five characters. '
            '[[slnc 300]] A version number. [[slnc 200]] The trace ID. '
            "[[slnc 200]] The caller's own span ID. [[slnc 200]] And a flag "
            'that says: keep this one. [[slnc 600]] Jaeger now holds one '
            'trace. [[slnc 300]] Eight spans, from two services, with one '
            'root. [[slnc 600]] Read as a family tree, the ranking model '
            "sits inside recommendations' span, which sits inside the page's "
            'call. [[slnc 300]] By its own time, the slowest piece of work '
            'is the ranking model: three hundred and forty milliseconds or '
            "more. [[slnc 600]] And the page's call lasted a little longer "
            'than recommendations took to answer. [[slnc 300]] That '
            'difference is the network hop itself. [[slnc 300]] You can only '
            'see it because both sides reported.'
        ),
    ),
    dict(
        key='06-tree', kind='diagram', title='One Page Load, One Trace',
        body=None,
        narration=(
            'So here is the shape of it. [[slnc 400]] The product page does '
            'its own four steps, and records six spans. [[slnc 300]] On its '
            'call to recommendations, it writes the trace parent header. '
            '[[slnc 300]] Recommendations reads that header, joins the same '
            'trace, and records two spans of its own. [[slnc 600]] Neither '
            'program ever holds the whole story. [[slnc 300]] Each sends its '
            'own spans to Jaeger, separately. [[slnc 300]] And Jaeger joins '
            'them by trace ID. [[slnc 600]] The rule is short. [[slnc 300]] '
            'Write the header on every call that leaves a program. [[slnc '
            '300]] Read it on every call that arrives.'
        ),
    ),
    dict(
        key='07-three', kind='console', title='The Collector Puts It Together, Later',
        body="""THREE. The collector puts it together, later.
  the customer has the page.
  Jaeger holds 0 spans of it.

  each service sends its finished spans
  in a batch, every 5 seconds.
  they arrive more than 2 seconds later.
  Jaeger then holds 8 spans:
  6 from product-page, 2 from recommendations.""",
        narration=(
            'Third demo: the collector puts it together, later. [[slnc 400]] '
            'The customer already has the page. [[slnc 300]] And at that '
            'moment, Jaeger holds none of its spans. [[slnc 600]] '
            'OpenTelemetry does not send a span the moment it ends. [[slnc '
            '300]] It keeps finished spans in memory, and sends them '
            'together, in a batch, every five seconds. [[slnc 300]] Sending '
            'each one as it finished would slow the shop down. [[slnc 600]] '
            'So the spans arrive more than two seconds after the customer '
            'had the page. [[slnc 300]] Then Jaeger holds eight: six sent by '
            'the product page, and two sent by recommendations. [[slnc 600]] '
            'The customer never waits for tracing. [[slnc 300]] That is the '
            'point. [[slnc 300]] And nobody sees the trace straight away. '
            '[[slnc 300]] That is the price.'
        ),
    ),
    dict(
        key='08-four', kind='console', title='Sampling At The Front Door',
        body="""FOUR. Sampling at the front door.
  keep one trace in 4, decided once,
  at the front door.
  20 page loads. kept: 6. dropped: 14.

  a kept load's header ends    -01
  a dropped load's header ends -00
  recommendations obeys the flag: 6 page loads.
  Jaeger holds 6 traces of the 20.
  a complaint about visit 1: no trace, ever.""",
        narration=(
            'Fourth demo: sampling at the front door. [[slnc 400]] Keeping '
            'every trace costs storage. [[slnc 300]] So the page now keeps '
            'one trace in four. [[slnc 300]] The decision is made once, at '
            'the front door. [[slnc 600]] Twenty page loads. [[slnc 300]] Six '
            'kept, and fourteen dropped. [[slnc 600]] The decision travels in '
            'the last two characters of the header. [[slnc 300]] Zero one '
            'means kept. [[slnc 300]] Zero zero means dropped. [[slnc 300]] '
            'Recommendations obeys the flag it is sent, and records spans '
            'for the same six. [[slnc 600]] Jaeger holds six traces of the '
            'twenty. [[slnc 300]] Now a customer complains about the first '
            'of those page loads. [[slnc 300]] Jaeger has no trace of it, '
            'and never will. [[slnc 300]] The decision was made at the only '
            'moment when nothing at all was known about that request.'
        ),
    ),
    dict(
        key='09-five', kind='console', title='A Clock That Is Off',
        body="""FIVE. A clock that is off.
  the recommendations machine: 3 seconds slow.
  the page's machine: right.

  Jaeger holds 1 trace: 8 spans, 1 root.
  the parent links are all correct.
  in start order, recommendations comes first:
  2 to 3 seconds before the call that caused it.
  Jaeger's warning: clock skew adjustment
  disabled. It corrects nothing.""",
        narration=(
            'Fifth demo: a clock that is off. [[slnc 400]] Each program '
            "stamps its spans with its own machine's time. [[slnc 300]] Now "
            "the recommendations machine's clock is set three seconds slow. "
            "[[slnc 300]] The page's clock is right. [[slnc 600]] The trace "
            'is complete. [[slnc 300]] Eight spans, one root, and every '
            'parent link is correct. [[slnc 300]] So the family tree is '
            'right. [[slnc 600]] But in time order, the first span is '
            "recommendations' own. [[slnc 300]] It starts two to three "
            'seconds before the call that caused it. [[slnc 300]] An answer, '
            'before its question. [[slnc 600]] Jaeger notices, and attaches '
            'a warning of its own. [[slnc 300]] Clock skew adjustment is '
            'turned off. [[slnc 300]] Out of the box, it stores what each '
            'service said, and corrects nothing.'
        ),
    ),
    dict(
        key='10-bill', kind='console', title='The Bill',
        body="""SIX. The bill.
  recommendations answers visit 6,
  then is killed before its next batch.
  Jaeger holds 6 spans of visit 6:
  6 from product-page, 0 from recommendations.

  every page load: 8 spans from 2 processes,
  and a 55-character header on every hop.
  Jaeger, out of the box: memory storage.""",
        narration=(
            'Sixth demo: the bill. [[slnc 400]] Recommendations answers the '
            'customer. [[slnc 300]] Then it is killed, before its next batch '
            'is sent. [[slnc 300]] The page stops politely, which sends '
            'everything it holds. [[slnc 600]] Jaeger holds six spans of '
            'that page load, all from the page. [[slnc 300]] None from '
            'recommendations. [[slnc 300]] Its spans were finished, correct, '
            'and waiting. [[slnc 300]] And they never arrive. [[slnc 600]] '
            'The spans a crash loses are always the last ones before it. '
            '[[slnc 300]] Exactly the ones somebody will want, when they '
            'investigate the crash. [[slnc 600]] And the ongoing costs. '
            '[[slnc 300]] Eight spans for every page load, from two '
            'programs. [[slnc 300]] A fifty-five character header on every '
            'hop. [[slnc 300]] And Jaeger is one more system to run. [[slnc '
            '300]] Out of the box, it keeps everything in memory, so a '
            'restart empties it.'
        ),
    ),
    dict(
        key='11-contrast', kind='bullets', title='What The Simulation Left Out',
        body=['Got right: spans, parents, one trace ID,', 'and the slowest step found by its own time.', '',
              'Left out: the hop as a header,', 'written and read by two programs.',
              'Left out: spans sent later, in batches.', 'Left out: a clock on every machine.', '',
              'Headline: a crash loses the last spans,', 'the ones about the crash.'],
        narration=(
            'So what did the plain Java version get right? [[slnc 400]] The '
            'whole idea. [[slnc 300]] Spans with parents, one trace ID, and '
            'the slowest step found by its own time. [[slnc 300]] All of '
            'that holds with Jaeger. [[slnc 600]] What it left out was the '
            'distance. [[slnc 300]] In the plain version, the trace was an '
            'object passed along inside one program. [[slnc 300]] Here, it '
            'has to become a header, cross the network, and be read by a '
            'different program. [[slnc 300]] Spans are sent later, in '
            'batches. [[slnc 300]] And every machine has its own clock. '
            '[[slnc 600]] And the headline. [[slnc 300]] In the plain '
            'version, a trace could never be lost. [[slnc 300]] Here, a '
            'crash loses exactly the spans you would want to read about the '
            'crash.'
        ),
    ),
    dict(
        key='12-verdict', kind='bullets', title='The Verdict',
        body=['Add a collector once one request', 'crosses more than one program.', '',
              '1. Write the header out, read it in.', '2. Sample once, at the front door.',
              '3. Shut down politely.', '4. Keep the clocks in step.',
              '5. Give the collector real storage.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Put a collector behind '
            'your services, as soon as one customer request crosses more '
            'than one program. [[slnc 600]] Then remember five things, '
            'because nothing will fail if you forget them. [[slnc 500]] One. '
            '[[slnc 200]] Write the header on every call that leaves a '
            'program, and read it on every call that arrives. [[slnc 400]] '
            'Two. [[slnc 200]] Sample once, at the front door, and let the '
            'decision travel. [[slnc 400]] Three. [[slnc 200]] Shut services '
            'down politely, so their last batch is sent. [[slnc 400]] Four. '
            "[[slnc 200]] Keep the machines' clocks in step. [[slnc 400]] "
            'Five. [[slnc 200]] Give the collector real storage, before you '
            'rely on it.'
        ),
    ),
    dict(
        key='13-recognise', kind='bullets', title='How To Recognise It',
        body=['inject(...) just before a request is sent.', 'extract(...) at the top of a handler.', '',
              'Sampler.parentBased(...):', 'follow the decision in the header.', '',
              'BatchSpanProcessor: how many seconds', 'of spans a crash can lose.'],
        narration=(
            'How can you spot this in code someone else wrote? [[slnc 400]] '
            'Look for a call to inject, just before a web request is sent. '
            '[[slnc 300]] And a call to extract, at the top of a request '
            'handler. [[slnc 300]] That is the header being carried. [[slnc '
            '600]] A sampler described as parent based means: follow the '
            'decision in the header, instead of making a new one. [[slnc '
            '600]] And a batch span processor, with its delay, tells you how '
            'many seconds of spans a crash can lose. [[slnc 600]] Where have '
            'you met this? [[slnc 300]] Spring Boot, Quarkus and the '
            'OpenTelemetry Java agent all write and read this header for '
            'you.'
        ),
    ),
    dict(
        key='14-real', kind='bullets', title='What Is Real, And When Not',
        body=['Real: OpenTelemetry 1.66.0,', 'Jaeger 2.21.0 in a container,', 'Testcontainers 2.0.5.', '',
              'Real: two Java processes, real HTTP,', 'traces read back from Jaeger.', '',
              'Too much: a shop that is one program.', 'A request ID in the logs is enough.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 400]] '
            'OpenTelemetry is version one point sixty-six. [[slnc 300]] '
            'Jaeger is version two point twenty-one, in a container that the '
            'demo starts and removes by itself. [[slnc 300]] The two '
            'services are separate Java programs, talking over real web '
            'requests. [[slnc 300]] And everything the demo says about a '
            'trace is read back from Jaeger itself, which neither service '
            'can fake. [[slnc 300]] You just need Docker switched on first. '
            '[[slnc 600]] So, when is this too much? [[slnc 300]] If the '
            'shop is one program, a profiler, or a request ID in the logs, '
            'answers the question without a collector to run. [[slnc 300]] '
            'A collector earns its keep once one request crosses several '
            'programs, and somebody has to say which of them was slow.'
        ),
    ),
    dict(
        key='15-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough',
              'are in the repository. Try the exercises in',
              'the session guide.'],
        narration=(
            "That's Distributed Tracing, with Jaeger. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] Give '
            'every request one trace ID, carry it across every hop, and '
            'remember that the trace arrives later, or not at all. [[slnc '
            '500]] The full source code, written notes, diagrams, and an '
            'animated walkthrough are all in the repository. [[slnc 500]] '
            'Here is one exercise to try. [[slnc 300]] Shorten the batch '
            'delay to one second, run the crash again, and count how many '
            'spans arrive. [[slnc 500]] If this helped, a like really does '
            'help other people find it. [[slnc 300]] And subscribe, if '
            "you'd like the rest of the series. [[slnc 400]] Thanks for "
            'watching.'
        ),
    ),
]
