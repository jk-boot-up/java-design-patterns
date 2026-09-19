package com.jk.explore.actorpattern;

import org.junit.jupiter.api.RepeatedTest;
import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.TimeUnit;

import static org.junit.jupiter.api.Assertions.*;

class ActorTest {

    @RepeatedTest(3)
    void sharedStateLosesAnUpdateWhenTwoThreadsReadBeforeEitherWrites() throws Exception {
        SharedStock s = new SharedStock("A", 10);
        CountDownLatch both = new CountDownLatch(2);
        Runnable r = () -> { both.countDown(); try { both.await(); } catch (InterruptedException e) { Thread.currentThread().interrupt(); } };
        Thread a = new Thread(() -> s.reserve("A", 3, r));
        Thread b = new Thread(() -> s.reserve("A", 4, r));
        a.start(); b.start(); a.join(); b.join();
        assertNotEquals(3, s.stockOf("A"));
        assertTrue(s.stockOf("A") == 6 || s.stockOf("A") == 7);
    }

    @RepeatedTest(3)
    void anActorLosesNothingUnderManySenders() throws Exception {
        try (InventoryActor inv = new InventoryActor(Map.of("A", 4000))) {
            inv.start();
            List<Thread> ts = new ArrayList<>();
            for (int i = 0; i < 4; i++) {
                Thread t = new Thread(() -> { for (int n = 0; n < 1000; n++) inv.tell(new Messages.Reserve("A", 1)); });
                ts.add(t);
                t.start();
            }
            for (Thread t : ts) t.join();
            assertEquals(0, inv.ask(new Messages.StockOf("A")).get(10, TimeUnit.SECONDS));
            assertEquals(4001, inv.handled());
        }
    }

    @Test
    void aReplyIsAMessageEvenWhenItIsARefusal() throws Exception {
        try (InventoryActor inv = new InventoryActor(Map.of("A", 5))) {
            inv.start();
            assertEquals(new Messages.Reserved("A", 3), inv.ask(new Messages.Reserve("A", 3)).get(5, TimeUnit.SECONDS));
            assertEquals(new Messages.OutOfStock("A", 3, 2), inv.ask(new Messages.Reserve("A", 3)).get(5, TimeUnit.SECONDS));
        }
    }

    @Test
    void theActorExposesNoWayToReadItsStockDirectly() {
        for (var m : InventoryActor.class.getDeclaredMethods()) {
            if (java.lang.reflect.Modifier.isPublic(m.getModifiers())) {
                assertFalse(m.getName().toLowerCase().contains("stock"), m.getName());
            }
        }
    }

    @Test
    void aBadMessageRestartsTheActorAndTheNextMessageIsHandled() throws Exception {
        try (InventoryActor inv = new InventoryActor(Map.of("A", 5))) {
            inv.start();
            inv.ask(new Messages.Reserve("A", 2)).get(5, TimeUnit.SECONDS);
            assertEquals(3, inv.ask(new Messages.StockOf("A")).get(5, TimeUnit.SECONDS));
            assertThrows(ExecutionException.class, () -> inv.ask(new Messages.Poison()).get(5, TimeUnit.SECONDS));
            assertEquals(1, inv.restarts());
            assertEquals(5, inv.ask(new Messages.StockOf("A")).get(5, TimeUnit.SECONDS));
        }
    }

    @Test
    void anUnknownMessageIsARestartNotACrashOfTheProgram() throws Exception {
        try (InventoryActor inv = new InventoryActor(Map.of("A", 5))) {
            inv.start();
            assertThrows(ExecutionException.class, () -> inv.ask("what?").get(5, TimeUnit.SECONDS));
            assertEquals(5, inv.ask(new Messages.StockOf("A")).get(5, TimeUnit.SECONDS));
        }
    }

    @Test
    void twoActorsWaitingForEachOtherNeverAnswer() throws Exception {
        assertEquals("no answer", ActorDemo.cycle());
    }
}
