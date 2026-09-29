# Dependencies

This project uses Selenium and a real Chromium browser in a container, which
the plain Java version of Page Object does not. Skipping it loses none of the
pattern: the plain version teaches all of it with nothing installed.

## What Selenium WebDriver is

Selenium drives a real browser from code. A WebDriver is one browser session; RemoteWebDriver talks to a browser in another process, here in a container. findElement with By.id finds an element and throws NoSuchElementException if it is missing. click and sendKeys act on it. WebDriverWait waits, up to a limit, for a condition such as some text appearing.

## What The browser container is

The selenium/standalone-chromium image runs Chromium with a WebDriver server on port 4444. Testcontainers starts it and lets it reach the shop's pages running on this machine.

## Why this project uses them

The plain version uses a pretend browser. This version shows the real thing,
where timing and missing elements are real, and why page objects are the
standard answer.

## What to install

Only a JDK, version 21, and a running Docker. Gradle downloads the rest, and the versions are pinned:

| Tool | Version |
| --- | --- |
| Java | 21 |
| Docker | running; 24 or later |
| Browser image | selenium/standalone-chromium:152.0 |
| Selenium | 4.49.0 |
| Testcontainers | 2.0.5 |

## What it costs

- A large browser image to download, and slow test runs.
- Page objects to maintain as the pages change.
