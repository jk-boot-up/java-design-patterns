package com.jk.explore.memoization;

import java.util.HashMap;
import java.util.Map;

/**
 * The cheapest way to buy n mugs with the shop's multi-buy offers: 1 for £4, 2 for £7, 3 for £10, 5 for £15.
 *
 * <p>The best price for n is the best of: one offer, plus the best price for
 * what is left. Written plainly, that asks the same smaller questions again and
 * again. The memoized version writes each answer down the first time.
 */
public final class MultiBuy {

    static final int[][] OFFERS = {{1, 400}, {2, 700}, {3, 1000}, {5, 1500}};

    private long calls;
    private final Map<Integer, Long> memo = new HashMap<>();

    /** Without the pattern: recomputes every smaller answer each time it is needed. */
    public long plain(int n) {
        calls++;
        if (n == 0) {
            return 0;
        }
        long best = Long.MAX_VALUE;
        for (int[] o : OFFERS) {
            if (o[0] <= n) {
                best = Math.min(best, o[1] + plain(n - o[0]));
            }
        }
        return best;
    }

    /** With the pattern: the same code, but each answer is remembered and reused. */
    public long memoized(int n) {
        Long known = memo.get(n);
        if (known != null) {
            return known;
        }
        calls++;
        long best = 0;
        if (n > 0) {
            best = Long.MAX_VALUE;
            for (int[] o : OFFERS) {
                if (o[0] <= n) {
                    best = Math.min(best, o[1] + memoized(n - o[0]));
                }
            }
        }
        memo.put(n, best);
        return best;
    }

    public long calls() {
        return calls;
    }
}
