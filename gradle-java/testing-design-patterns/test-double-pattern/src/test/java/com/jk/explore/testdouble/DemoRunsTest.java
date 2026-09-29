package com.jk.explore.testdouble;

import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;
import org.junit.jupiter.api.Test;

/** Every number the demo prints, checked, so the video and docs can quote them. */
class DemoRunsTest {

    private final String all = String.join("\n", TestDoubleDemo.run());

    private void prints(String text) {
        assertTrue(all.contains(text), () -> "missing: " + text);
    }

    @Test
    void theRealProviderAct() {
        prints("3 tests passed, taking 2400 ms of network calls");
        prints("real money charged to the test card: £88.42");
        prints("FAILED, network unreachable");
    }

    @Test
    void theDoubleActs() {
        prints("fails if touched: refused: the basket is empty");
        prints("a stub that always declines: not paid: insufficient funds");
        prints("the spy recorded: [charge(ORD-7, 6344), refund(spy-1)]");
        prints("expected charge(ORD-8, 6344): paid, receipt mock-1");
        prints("FAILED at once, unexpected call: charge(ORD-8, 6344), no more charges were expected");
        prints("pay another £50.00: not paid: over the card limit");
        prints("pay £50.00 again: paid, receipt fake-2; balance £50.00");
    }

    @Test
    void theBill() {
        prints("tested with a stub: paid, receipt stub-1, PASSED");
        prints("recorded [charge(ORD-12, 63)], not charge(ORD-12, 6344): FAILED");
    }

    @Test
    void sixActsInOrder() {
        int last = -1;
        for (String act : List.of("ONE.", "TWO.", "THREE.", "FOUR.", "FIVE.", "SIX.")) {
            int at = all.indexOf(act);
            assertTrue(at > last, act);
            last = at;
        }
    }
}
