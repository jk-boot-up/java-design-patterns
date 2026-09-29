package com.jk.explore.money;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;
import org.junit.jupiter.api.Test;

/** Every number the demo prints, checked, so the video and docs can quote them. */
class DemoRunsTest {

    private final List<String> out = MoneyDemo.run();

    private void prints(String text) {
        assertTrue(out.stream().anyMatch(l -> l.contains(text)), () -> "missing: " + text);
    }

    @Test
    void theDoublesAreWrongInTheWaysTheActsSay() {
        prints("total 0.30000000000000004");
        prints("is it 0.30? false");
        prints("1000 items at 10p, added one by one: 99.9999999999986");
        prints("9999 pence, not 10000");
    }

    @Test
    void moneyIsExact() {
        prints("10p + 20p = £0.30, equal to 30p: true");
        prints("1000 items at 10p: £100.00, stored as 10000 pence");
        prints("2 coasters at £4.99: £63.44");
    }

    @Test
    void currenciesAndDigitsAreChecked() {
        prints("£10.00 + $10.00: refused, cannot combine GBP with USD");
        prints("¥1500");
        prints("£9.999: refused");
    }

    @Test
    void roundingOnceDiffersFromRoundingEachLine() {
        prints("rounded on each line: £2.00");
        prints("rounded once on the total:            £1.98");
        prints("difference: £0.02");
    }

    @Test
    void splittingLosesNothing() {
        prints("£3.33 x 3 = £9.99, a penny short");
        prints("allocate(1, 1, 1): £3.34, £3.33, £3.33 = £10.00");
        prints("£2.25, £1.97, £0.78 = £5.00");
    }

    @Test
    void sixActsInOrder() {
        String all = String.join("\n", out);
        int last = -1;
        for (String act : List.of("ONE.", "TWO.", "THREE.", "FOUR.", "FIVE.", "SIX.")) {
            int at = all.indexOf(act);
            assertTrue(at > last, act);
            last = at;
        }
        assertFalse(all.contains("was allowed"));
    }
}
