# Problem Statement

## The scenario

The product page shows product details, a basket summary and
recommendations, built by three teams.

## The naive version

`OneFrontEnd` renders everything in one application: one team's bug fails the
whole page, and every release includes everyone's code.

## What this project must deliver

- One front-end shown failing as a whole.
- Three team apps serving fragments over HTTP, assembled into one page.
- Failing and slow fragments replaced by fallbacks.
- One team releasing on its own.
- The costs shown: extra requests and inconsistent formats.
- Every printed result asserted by a test.
