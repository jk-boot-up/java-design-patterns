package com.jk.explore.eventsourcingeventstoredb;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import org.junit.jupiter.api.Test;

/**
 * The demo is the document. Every number quoted in the README, in the slides and in the narration
 * is asserted here, so a change that moves a figure fails the build instead of quietly making the
 * documents wrong.
 */
class DemoRunsTest {

    private static final String[] QUOTED = {
        "4 events appended to the stream loyalty-C-4417. KurrentDB numbered them revision 0 to 3.",
        "revision 0  2025-03-01  earned 60 points on order ORD-8801",
        "revision 1  2025-03-03  spent 25 points on order ORD-8814",
        "revision 2  2025-03-08  earned 120 points on order ORD-8907",
        "revision 3  2025-03-14  lost 15 points to the twelve-month expiry",
        "balance: 140 points, from 4 events. nothing stores 140; it was added up just now.",
        "it has no call that changes one event.",
        "C-5120 has 140 points. the website and the phone app both look: 140 points, at revision 3.",
        "both decide 100 is not more than 140, and both append a redemption with the check off.",
        "both appends accepted, at revisions 4 and 5. balance now: -60 points.",
        "the customer spent 200 points they had only 140 of",
        "C-5121 has 140 points. both checkouts look: 140 points, at revision 3. both append, expecting revision 3.",
        "appends accepted: 1, at revision 4. appends refused: 1.",
        "the refusal is WrongExpectedVersion: expected revision 3, but the stream is at revision 4.",
        "the refused checkout looks again: 40 points, at revision 4. 100 is more than 40, so it tells the customer no.",
        "balance now: 40 points. nothing was locked; the server compared one number.",
        "the shop awards C-5122 45 points for order ORD-9001, loses the reply, and sends the award again.",
        "sent again with a new event id: 2 awards for ORD-9001 in the stream. balance 90.",
        "for C-5123 the first send is written at revision 0, expecting a stream that does not exist yet.",
        "the server answers revision 0 again, and writes nothing.",
        "1 award in the stream. balance 45.",
        "it receives 18 events that were already stored, and the server tells it it has caught up.",
        "it shows C-4417 = 140, C-5120 = -60, C-5121 = 40, C-5122 = 90.",
        "moments later the dashboard shows C-4417 = 160, with 19 events received in all.",
        "reading the stream now: stream not found.",
        "2 events of loyalty-C-5122 are still there, until a clean-up called a scavenge runs.",
        "the support dashboard still shows C-5122 = 90.",
        "it is accepted at revision 2, not 0, and reading the stream shows 1 event.",
        "no TLS, no passwords, in 1 container.",
    };

    @Test
    void theSixActsRunAgainstARealKurrentDBAndPrintTheFiguresTheDocumentsQuote() {
        assumeTrue(KurrentServer.containerRuntimeAvailable(), "needs a container runtime");
        String out = runTheDemo();
        for (String act : new String[]{"ONE.", "TWO.", "THREE.", "FOUR.", "FIVE.", "SIX."}) {
            assertTrue(out.contains(act), out);
        }
        for (String line : QUOTED) {
            assertTrue(out.contains(line), "missing: " + line + "\n" + out);
        }
    }

    @Test
    void aSecondRunPrintsExactlyTheSameThing() {
        assumeTrue(KurrentServer.containerRuntimeAvailable(), "needs a container runtime");
        assertEquals(runTheDemo(), runTheDemo());
    }

    private static String runTheDemo() {
        PrintStream original = System.out;
        ByteArrayOutputStream captured = new ByteArrayOutputStream();
        try {
            System.setOut(new PrintStream(captured, true, StandardCharsets.UTF_8));
            EventSourcingWithKurrentDemo.main(new String[0]);
        } finally {
            System.setOut(original);
        }
        return captured.toString(StandardCharsets.UTF_8);
    }
}
