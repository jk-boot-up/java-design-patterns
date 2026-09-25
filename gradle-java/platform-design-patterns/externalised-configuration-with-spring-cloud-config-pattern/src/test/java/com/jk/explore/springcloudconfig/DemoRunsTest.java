package com.jk.explore.springcloudconfig;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import org.junit.jupiter.api.Test;

/**
 * The demo is the document. Every figure the README, the slides and the narration quote is
 * asserted here, so a change that alters a figure fails the build instead of quietly making the
 * documents wrong.
 */
class DemoRunsTest {

    @Test
    void theSixActsPrintTheFiguresTheDocumentsQuote() throws IOException {
        String out = runTheDemo();
        String[] expected = {
            "Act 1 - the setting lives in git, and a config server hands it out over HTTP",
            "  git commit 2a6198d by Priya in engineering: free-over 50.00",
            "    version 2a6198d, delivery.free-over 50.0",
            "    quote:  goods £48.00 delivery £4.99 threshold £50.00",
            "    banner: Free delivery on orders over £50.00",
            "Act 2 - marketing commits a weekend promotion: free delivery over 35.00",
            "  git commit 64f6a92 by Maya in marketing: free-over 35.00",
            "    version 64f6a92, delivery.free-over 35.0",
            "  committed, and served, but not in force.",
            "Act 3 - the refresh: POST /actuator/refresh, and no restart",
            "  the shop fetches again and reports what changed: config.client.version, delivery.free-over",
            "    quote:  goods £48.00 delivery FREE threshold £35.00",
            "  the same running shop: yes, still the copy started in act 1. restarts: 0.",
            "Act 4 - the surprise: the refresh reached the checkout, and not the banner",
            "  one running shop, two thresholds.",
            "    banner: Free delivery on orders over £35.00",
            "Act 5 - the bill: somebody commits -1 on Saturday morning",
            "  git commit 6aaf4da by Maya in marketing: free-over -1",
            "    version 6aaf4da, delivery.free-over -1",
            "  the refresh answers 200 and reports: config.client.version, delivery.free-over",
            "  the next 5 quotes: 5 failed, each with HTTP status 500.",
            "  git commit f68331f by Sam on call: free-over 35.00, then a refresh: config.client.version, delivery.free-over",
            "    f68331f  Sam on call  Put the weekend promotion back",
            "    6aaf4da  Maya in marketing  Free delivery for everyone?",
            "    64f6a92  Maya in marketing  Weekend promotion: free delivery over 35 pounds",
            "    2a6198d  Priya in engineering  Free delivery over 50 pounds",
            "Act 6 - the bill: the config server stops",
            "  a refresh of the running shop now answers 500.",
            "    refused to start: Could not locate PropertySource and the fail fast property is set, failing",
            "  it started on the default packed inside it. the promotion is gone, with no error.",
            "stopped: the config server process, and all 3 copies of the shop that started. still running: 0.",
        };
        for (String line : expected) {
            assertTrue(out.contains(line), "missing: " + line + "\n" + out);
        }
        // Act 4: the checkout moved to £35.00 while the banner in the same shop still says £50.00.
        String act4 = out.substring(out.indexOf("Act 4"), out.indexOf("after a restart"));
        assertTrue(act4.contains("threshold £35.00"), act4);
        assertTrue(act4.contains("over £50.00"), act4);
        // Act 6: the running shop keeps £35.00, the optional newcomer is back on £50.00.
        String act6 = out.substring(out.indexOf("Act 6"));
        assertTrue(act6.contains("delivery FREE threshold £35.00"), act6);
        assertTrue(act6.contains("delivery £4.99 threshold £50.00"), act6);
        assertEquals(0, Shop.running());
    }

    private static String runTheDemo() throws IOException {
        PrintStream original = System.out;
        ByteArrayOutputStream captured = new ByteArrayOutputStream();
        try {
            System.setOut(new PrintStream(captured, true, StandardCharsets.UTF_8));
            SpringCloudConfigDemo.main(new String[0]);
        } finally {
            System.setOut(original);
        }
        return captured.toString(StandardCharsets.UTF_8);
    }
}
