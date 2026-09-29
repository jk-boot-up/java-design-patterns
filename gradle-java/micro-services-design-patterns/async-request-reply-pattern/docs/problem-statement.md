# Problem Statement

## The scenario

Sellers ask for a monthly sales report that takes six seconds to build. The
gateway in front of the store gives up on any request after three seconds.

## The naive version

`SyncReportApi` builds the report while the request waits. The gateway answers
504 after three seconds, the seller clicks again, and the server builds the
report again for nobody.

## What this project must deliver

- The timeout shown: two 504s, two builds, nothing received.
- A submit that answers 202 Accepted at once with a status link and a retry hint.
- Status checks showing progress, then 303 See Other to the result.
- A repeated submit with the same key returning the same job, built once.
- The costs shown: 5 requests instead of 1, and 62 for an impatient client.
- Every printed number asserted by a test.
