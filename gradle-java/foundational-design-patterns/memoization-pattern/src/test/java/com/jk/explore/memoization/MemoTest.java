package com.jk.explore.memoization;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

class MemoTest {

    @ParameterizedTest
    @ValueSource(ints = {0, 1, 2, 3, 4, 5, 7, 11, 18})
    void memoizedAgreesWithPlain(int n) {
        assertEquals(new MultiBuy().plain(n), new MultiBuy().memoized(n));
    }

    @Test
    void memoizedCallsOncePerSize() {
        MultiBuy m = new MultiBuy();
        m.memoized(25);
        assertEquals(26, m.calls());
    }

    @Test
    void memoCallsTheSlowFunctionOncePerArgument() {
        Memo<String, Long> memo = new Memo<>(ShippingQuotes::quote);
        memo.apply("LS1");
        memo.apply("LS1");
        memo.apply("BA2");
        assertEquals(2, memo.slowCalls());
    }

    @Test
    void memoOfImpureFunctionGoesStale() {
        ShippingQuotes.Euros e = new ShippingQuotes.Euros();
        Memo<Long, Long> memo = new Memo<>(e::convert);
        long before = memo.apply(100L);
        e.setRate(200);
        assertEquals(before, memo.apply(100L));
    }
}
