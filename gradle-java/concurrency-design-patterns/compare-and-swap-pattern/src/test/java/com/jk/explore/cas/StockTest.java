package com.jk.explore.cas;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;

import org.junit.jupiter.api.RepeatedTest;
import org.junit.jupiter.api.Test;

class StockTest {

    @RepeatedTest(3)
    void casNeverOversells() throws Exception {
        CasStock s = new CasStock(50);
        assertEquals(50, FlashSale.run(6, 20, s::buyOne));
        assertEquals(0, s.left());
    }

    @RepeatedTest(3)
    void getAndUpdateNeverOversells() throws Exception {
        CasStock s = new CasStock(50);
        assertEquals(50, FlashSale.run(6, 20, s::buyOneShort));
    }

    @Test
    void lockNeverOversells() throws Exception {
        LockedStock s = new LockedStock(30);
        assertEquals(30, FlashSale.run(4, 20, s::buyOne));
    }

    @Test
    void emptyStockSellsNothing() {
        CasStock s = new CasStock(0);
        assertFalse(s.buyOne());
        assertFalse(s.buyOneShort());
    }
}
