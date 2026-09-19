package com.jk.explore.monitorobject;

import com.jk.explore.monitorobject.harness.Rendezvous;
import com.jk.explore.monitorobject.naive.VolatileStock;
import org.junit.jupiter.api.RepeatedTest;

import static org.junit.jupiter.api.Assertions.assertEquals;

class VolatileStockTest {

    @RepeatedTest(20)
    void volatileDoesNotPreventTheLostUpdate() throws InterruptedException {
        Rendezvous bothRead = new Rendezvous("both-read", 2);
        VolatileStock stock = new VolatileStock(10, bothRead::meet);
        Thread a = new Thread(stock::sellOne);
        Thread b = new Thread(stock::sellOne);
        a.start();
        b.start();
        a.join(5_000);
        b.join(5_000);
        assertEquals(9, stock.available(), "volatile gives visibility, not atomicity");
    }
}
