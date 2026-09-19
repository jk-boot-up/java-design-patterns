package com.jk.explore.monitorobject;

import com.jk.explore.monitorobject.harness.Rendezvous;
import com.jk.explore.monitorobject.naive.CallerLockedStock;
import org.junit.jupiter.api.RepeatedTest;

import static org.junit.jupiter.api.Assertions.assertEquals;

class CallerLockedStockTest {

    @RepeatedTest(20)
    void oneForgetfulCallerCorruptsWhatACarefulCallerProtected() throws InterruptedException {
        Rendezvous bothRead = new Rendezvous("both-read", 2);
        CallerLockedStock stock = new CallerLockedStock(10, bothRead::meet);
        Thread careful = new Thread(() -> {
            stock.lock().lock();
            try {
                stock.sellOne();
            } finally {
                stock.lock().unlock();
            }
        });
        Thread forgetful = new Thread(stock::sellOne);
        careful.start();
        forgetful.start();
        careful.join(5_000);
        forgetful.join(5_000);
        assertEquals(9, stock.available());
    }
}
