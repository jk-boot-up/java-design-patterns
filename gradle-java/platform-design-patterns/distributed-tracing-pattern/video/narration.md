# Distributed Tracing Pattern — Video Narration Script

## 1. Distributed Tracing

Hello, and welcome. This video explains the Distributed Tracing pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. Distributed tracing gives one customer request a single I D. Then every piece of work done for that request records two things. How long it took. And which piece of work asked for it. Think of a hospital. At reception you get a wristband with a number. It follows you to X-ray, to the blood test, and to the doctor. Each department's form carries your number, and says who sent you. So afterwards, someone can rebuild your whole afternoon, in order. In our online store, a product page takes nine hundred milliseconds. Four healthy services helped build it, and nobody can say which one is slow. By the end, you will know why merged logs cannot answer that. The one subtraction that names the culprit. And three ways this pattern quietly stops telling the truth.

## 2. The Scenario

Here is the scenario. A customer opens the page for one product. It takes nine hundred milliseconds, slow enough to notice. Four services helped build that page. Catalog looked up the product. Pricing worked out the price. Inventory checked the stock. And recommendations built a list of other things to buy. All four services are up. All four are writing logs, and all the logs are correct. Nothing is broken, and nothing is alerting. But nobody can say which service spent the nine hundred milliseconds.

## 3. What the Logs Give You

So let's read the logs. All four services write them, and a tool has merged them, in time order. Two customers happen to be on the site at the same moment. That is normal. So there are two lines saying pricing started a quote. And two lines saying pricing finished one. Now: how long did pricing take? Match the first finish with the first start, and it is a hundred and eighty milliseconds. Match the other finish, and it is two hundred and twenty. Both look reasonable. But one of them subtracts one customer's start from another customer's finish. Every timestamp is correct. And nothing tells you which lines belong together.

## 4. More Logging Does Not Fix It

The natural reaction is to log more. So let's try it. Add the thread name. That fails as soon as the work moves to another thread. Add the machine name. Both customers were served by the same machine. Add the product. Both customers viewed the same product. Every idea fails the same test. You need something that is the same for everything done for one request. And different for the next request. So what is missing is not more detail. It is an I D.

## 5. The Pattern

Here is the pattern, in two parts. First, give each customer request one I D, created at the front door. Everything that happens because of that request carries it. That is called the trace I D. Second, every piece of work records four things. What it was. When it started. How long it lasted. And the I D of the piece of work that asked for it. Each of those records is called a span. And that last field is called the parent. The first part lets you filter the logs down to one customer. The second part turns them into an answer. Because once every span knows its parent, the shape of the whole request can be rebuilt afterwards, by anyone.

## 6. Three Moves

In practice, that is three moves. Move one. The first service creates an I D, and passes it on with every call it makes. It travels as two small values: the trace I D, and the I D of the span doing the calling. Move two. Each piece of work opens a span when it starts, and closes it when it finishes. The span is only recorded when it closes, because only then is its length known. A span that is never closed does not appear at all. Move three, the one people get wrong. When one service calls another, the new span must be started from the caller's own span. Not from the page's. That one choice is the difference between a useful trace and a misleading one.

## 7. Who Does What

Let's name the pieces. There are six, and they are all small. A trace context: the two I Ds that travel with the request. A span: one piece of work, with a name, a start, a length, and a parent. A tracer: it hands out spans, and times them. A trace: all the spans for one request. It does the arithmetic: which span is the first, which spans belong to which, and how much time each spent on its own work. A drawing, which turns a trace into a picture. The picture is built only from the parent field. And the sixth piece is the merged log. It is not part of the pattern. It is what the pattern replaces.

## 8. The One Argument That Is the Pattern

Here is the one piece of code that matters, in words. The page opens a span called recommendations. It starts it from the page's own span. So recommendations becomes a child of the page. Inside it, a second span is opened, for the ranking model. And this one is started from recommendations' span, not the page's. So the ranking model is a child of recommendations, one level deeper. Now here is the key point. If you started it from the page's span by mistake, the program would still run. The total would still be nine hundred milliseconds. Everything would still add up. And the answer would be wrong. A trace can be perfectly consistent, and still false.

## 9. Seven Spans, and the Column That Matters

Let's run it. One page load now produces seven spans. Here is each span's parent. Catalog's parent is span one, the page. So are pricing, inventory, render, and recommendations. The ranking model is the odd one out. Its parent is span five: recommendations. And the page itself has no parent at all. Exactly one span per request has no parent. It is called the root. This is still just a list. But it holds enough to rebuild the whole request, exactly as it happened.

## 10. The Waterfall — That Column, Drawn

Here are the same seven spans, drawn as a picture called a waterfall. Let's describe it in words. The top line is the page. Its bar runs the full nine hundred milliseconds. One level below it, the bars appear in order, left to right. Catalog, a hundred and twenty milliseconds, right at the start. Pricing, a hundred and eighty. Inventory, ninety. Recommendations, four hundred, by far the widest. And render, a hundred and ten, at the end. One level deeper, inside recommendations, sits the ranking model: three hundred and forty. Nobody designed that shape. The indenting comes from the parent field. The position comes from the start time. When a tracing tool shows a picture like this, it is showing your own data.

## 11. Self Time — The Whole Trick

Now the arithmetic. It is one subtraction, and it is the whole trick. A span's length is how long it lasted. Its self time is its length, minus the length of its children. In other words, the time it was working, not waiting. Apply that to the page. It lasted the full nine hundred milliseconds, so it always looks biggest. But its self time is zero. It did nothing. It waited. Think of a manager whose whole day was spent in other people's meetings. The longest day on the team, and no work of their own. Recommendations lasted four hundred milliseconds. But only sixty were its own. The other three hundred and forty belong to the ranking model. So the ranking model is the top of the list. Three hundred and forty milliseconds, thirty-seven percent of the customer's wait. The question from the start is answered, by subtraction, afterwards.

## 12. The Bill, Part One — A Service That Opens No Span

That is the pattern, and it works. Now the bill, with three items. Item one: a service that opens no span. Recommendations never records a span of its own. But it still passes the trace I D on to the ranking model. So nothing fails, and nothing warns. Listen to what happens. Now there are six spans, not seven. The ranking model appears directly under the page, as if the page called it. Nothing in the code does that. And sixty milliseconds land on the page. So the page now seems to do sixty milliseconds of its own work. It does none. By every check you might run, this trace looks healthy. But the service really responsible is missing. And someone spends the afternoon investigating the page instead. That is why partial tracing is worse than none. None tells you nothing. Partial tells you something false, with confidence.

## 13. The Bill, Part Two — One Line, in the Wrong Place

Item two: one line in the wrong place. The recommendations call is moved onto a separate worker thread. So the page can do other things while it runs. A sensible change. But the trace I D is kept in a variable that belongs to one thread only. The page's thread has it. The worker thread never did. So the worker's span has no parent. Now there are two roots in one trace. The page, and recommendations, side by side. Four hundred milliseconds of work that belong to nobody. No error. No warning. The fix is to move one line earlier. Read the trace I D on the thread that has it. And hand it to the worker as an ordinary value. Now there is one root, with recommendations under it, where it belongs. The broken and working versions differ by one line, in a different place.

## 14. The Bill, Part Three — The Decision Made Too Early

Item three: a decision made too early. Storing every span is expensive. So the front door keeps only one trace in every hundred. And throws the rest away. Out of a million requests today, ten thousand traces are kept. Nine hundred and ninety thousand are gone. Then a customer complains about one particular slow page. Its trace was not kept. It is gone for good. It was thrown away at the front door, before anyone knew it would be slow. So a one percent sample can tell you recommendations is slow on average. But it cannot tell you why this one request was slow. The way out is called tail sampling. Hold the spans briefly, let the request finish, and then keep the trace if it was slow, or if it failed. The decision moves to the end, the only place it can be made well.

## 15. What to Take Away

Here are three things to remember. One. A trace I D makes the logs readable. A parent I D turns them into an answer. Two. Look at self time, not total time. The longest span is always the request itself, and it is always innocent. Three. The trace I D gets lost at boundaries: threads, queues, and scheduled jobs. Pass it as an ordinary value. And one boundary worth knowing. Tracing is one of three tools, with logs and metrics. Logs answer: what was the error? Metrics answer: how does today compare with yesterday? Traces answer: where did the time go, in this one request? Many teams try to make logs do all three. That is exactly where this video started: four correct logs, and no answer.

## 16. Thanks for Watching

That's the Distributed Tracing pattern. If you remember one sentence, make it this one. One I D for the request, one parent for every piece of work, and a subtraction that turns them into an answer. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Both the broken and the working version of every failure are there to run. Here is one exercise to try. Find one place in your own code where work is handed to another thread. And check whether the trace I D makes the trip. If you found this useful, a like really helps other people discover it. Kindly subscribe to the channel. It helps the channel grow and bring you more content. Thanks for watching!
