# Distributed Tracing with Jaeger Pattern — UML Sequence Diagrams

Four sequences. The late batch and the crash come first, because they are the headline find and the one thing a trace kept in the demo's own memory could never show.

## 1. The Spans Arrive Later, Or Never

The customer has the page before Jaeger holds any of it. A service killed before its next batch never sends its spans at all.

![The spans arrive later, or never](images/uml-diagram.png)

## 2. A Hop That Forgets The Header

The page calls recommendations with no traceparent. Recommendations starts a trace of its own, and one page load becomes two traces, each looking complete.

![A hop that forgets the header](images/uml-diagram-2.png)

## 3. Sampling At The Front Door

The page keeps one trace in four. The decision travels in the header's flags, and recommendations obeys it.

![Sampling at the front door](images/uml-diagram-3.png)

## 4. A Clock That Is Off

The recommendations machine's clock is 3 seconds slow. The parent links are right; the times are not, and Jaeger only warns.

![A clock that is off](images/uml-diagram-4.png)

