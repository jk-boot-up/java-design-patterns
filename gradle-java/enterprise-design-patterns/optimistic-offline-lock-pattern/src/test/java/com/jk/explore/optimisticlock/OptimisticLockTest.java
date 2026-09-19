package com.jk.explore.optimisticlock;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class OptimisticLockTest {

    private static final Product MUG = OptimisticLockDemo.MUG;

    @Test
    void withNoLockTheLastWriteSilentlyWins() {
        LastWriteWinsStore s = new LastWriteWinsStore();
        s.insert(MUG);
        Product a = s.load("MUG-BLUE");
        Product b = s.load("MUG-BLUE");
        s.save(a.withPrice(1200));
        s.save(b.withStock(40));
        assertEquals(1000, s.load("MUG-BLUE").pricePence());
    }

    @Test
    void aStaleSaveIsRefusedAndTheFirstWriteSurvives() {
        OptimisticStore s = new OptimisticStore();
        s.insert(MUG);
        var a = s.load("MUG-BLUE");
        var b = s.load("MUG-BLUE");
        s.save(a.with(a.value().withPrice(1200)));
        assertThrows(StaleWrite.class, () -> s.save(b.with(b.value().withStock(40))));
        assertEquals(1200, s.load("MUG-BLUE").value().pricePence());
        assertEquals(50, s.load("MUG-BLUE").value().stock());
    }

    @Test
    void everySuccessfulSaveBumpsTheVersion() {
        OptimisticStore s = new OptimisticStore();
        s.insert(MUG);
        assertEquals(1, s.load("MUG-BLUE").version());
        var v = s.load("MUG-BLUE");
        var next = s.save(v.with(v.value().withStock(1)));
        assertEquals(2, next.version());
        assertEquals(2, s.load("MUG-BLUE").version());
    }

    @Test
    void reloadingAndReapplyingKeepsBothChanges() {
        OptimisticStore s = new OptimisticStore();
        s.insert(MUG);
        var b = s.load("MUG-BLUE");
        var a = s.load("MUG-BLUE");
        s.save(a.with(a.value().withPrice(1200)));
        assertEquals(2, OptimisticLockDemo.saveWithRetry(s, "MUG-BLUE", p -> p.withStock(40), b));
        assertEquals(new Product("MUG-BLUE", 1200, 40), s.load("MUG-BLUE").value());
    }

    @Test
    void changesToDifferentFieldsStillConflictBecauseTheVersionIsPerRow() {
        OptimisticStore s = new OptimisticStore();
        s.insert(MUG);
        var price = s.load("MUG-BLUE");
        var stock = s.load("MUG-BLUE");
        s.save(price.with(price.value().withPrice(1200)));
        assertThrows(StaleWrite.class, () -> s.save(stock.with(stock.value().withStock(40))));
    }

    @Test
    void tenWritersOnOneRowLoseNothingAndRepeatNineOfTheSaves() {
        OptimisticStore s = new OptimisticStore();
        s.insert(new Product("MUG-BLUE", 1000, 0));
        var reads = new java.util.ArrayList<Versioned<Product>>();
        for (int i = 0; i < 10; i++) reads.add(s.load("MUG-BLUE"));
        int attempts = 0;
        for (int i = 0; i < 10; i++) attempts += OptimisticLockDemo.saveWithRetry(s, "MUG-BLUE", p -> p.withStock(p.stock() + 1), reads.get(i));
        assertEquals(10, s.load("MUG-BLUE").value().stock());
        assertEquals(19, attempts);
    }

    @Test
    void aLongEditIsDiscardedWholeWhenItIsFinallySaved() {
        OptimisticStore s = new OptimisticStore();
        s.insert(MUG);
        var editor = s.load("MUG-BLUE");
        var other = s.load("MUG-BLUE");
        s.save(other.with(other.value().withPrice(900)));
        assertThrows(StaleWrite.class, () -> s.save(editor.with(editor.value().withStock(45))));
    }
}
