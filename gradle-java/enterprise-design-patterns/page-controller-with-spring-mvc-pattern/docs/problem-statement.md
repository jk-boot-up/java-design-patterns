# Problem Statement

## The scenario

The shop's pages were served by one handler that grew a branch per page.

## The naive version

Code for one page runs for every page, and every new page edits the shared
handler.

## What this project must deliver

- One handler crashing on a page it was not written for.
- A @RestController per page.
- Spring's parameter conversion and status exceptions.
- A new page as a new class.
- A forgotten login check, fixed by an interceptor.
- Every printed result asserted by a test.
