# Asynchronous Request-Reply, Explained

## The pattern in one sentence

Asynchronous Request-Reply accepts slow work at once with 202 and a status
link, lets the caller check back when told, and sends it on to the result when
the work is done.

## The 5 acts

### 1. Waiting for a slow report

`SyncReportApi` builds the report while the request waits. The report takes six
seconds; the gateway in front gives up after three and answers
`504 Gateway Timeout`. The seller clicks again and gets another 504. The server
never knew the seller had gone, so it built the report both times: two builds,
and the seller received nothing.

### 2. Accepted at once

`AsyncReportApi.submit` starts the job and answers immediately with
`202 Accepted`. The answer carries two things: a status link,
`/reports/status/R-1`, and a hint to check again after two seconds. The
connection closes straight away, so no gateway ever times out.

### 3. Check back, then fetch

`PollingClient` waits the two seconds it was told, then checks the status link:
running, 33 percent. Two seconds later: running, 66 percent. At six seconds the
status link answers `303 See Other`, pointing at `/reports/R-1`. The client
follows it and gets the report: 412 orders, £18,240.50.

### 4. Asking twice

Every submit carries a request key, here `seller-7-september`. The server keeps
a map from key to job, so a second submit with the same key returns the same
status link, `R-1`, and does not start the work again. The report is built
exactly once.

### 5. The bill

One report now costs five requests: submit, three status checks and a fetch.
A client that ignores the retry hint and checks every tenth of a second sends
62 requests for the same report. And the server must keep each job's state
until its result is collected, then clean it up.

## The verdict

Use it for any work that can take longer than a few seconds behind HTTP:
reports, exports, video processing, provisioning. Give each request a key so
a repeat does not start the work again, send a Retry-After hint, and clean up
finished jobs. When the client can receive a callback, prefer that to polling.

## How to recognise this in code you did not write

- An endpoint answering `202 Accepted` with a `Location` header.
- URLs like `/operations/{id}`, `/jobs/{id}` or `/status/{id}`.
- A `Retry-After` header on a status response.
- Client code that loops, sleeps, and checks a status field until it says done.

## Where you have already met this

- HTTP `202 Accepted` with a `Location` header, and `Retry-After`.
- Cloud APIs for long jobs: starting a virtual machine, transcoding a video, or an Azure long-running operation.
- "Your export is being prepared; we will show it here when it is ready" in many web apps.
- Payment providers that return `pending` and let you check the payment's status later.
