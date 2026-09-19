package com.jk.explore.monitorobject;

import com.jk.explore.monitorobject.harness.Rendezvous;
import com.jk.explore.monitorobject.naive.PlainStock;
import org.junit.jupiter.api.RepeatedTest;

import static org.junit.jupiter.api.Assertions.assertEquals;

class PlainStockTest {

    @RepeatedTest(20)
    void twoSalesLoseOneUpdateEveryRun() throws InterruptedException {
        Rendezvous bothRead = new Rendezvous("both-read", 2);
        PlainStock stock = new PlainStock(10, bothRead::meet);
        Thread a = new Thread(stock::sellOne);
        Thread b = new Thread(stock::sellOne);
        a.start();
        b.start();
        a.join(5_000);
        b.join(5_000);
        assertEquals(9, stock.available(), "two sales, one lost update");
    }
}
