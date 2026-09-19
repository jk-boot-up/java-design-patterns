package com.jk.explore.monitorobject;

import com.jk.explore.monitorobject.pattern.IfInsteadOfWhile;
import org.junit.jupiter.api.RepeatedTest;

import static org.junit.jupiter.api.Assertions.assertEquals;

class IfInsteadOfWhileTest {

    @RepeatedTest(20)
    void checkingOnceSellsAnItemThatWasNeverThere() throws InterruptedException {
        assertEquals(-1, IfInsteadOfWhile.twoTakersOneItem(new IfInsteadOfWhile.BrokenStock()));
    }
}
