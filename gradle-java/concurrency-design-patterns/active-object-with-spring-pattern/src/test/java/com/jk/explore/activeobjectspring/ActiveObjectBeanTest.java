package com.jk.explore.activeobjectspring;

import org.junit.jupiter.api.Test;
import org.springframework.context.ConfigurableApplicationContext;
import org.springframework.core.task.TaskRejectedException;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.CompletionException;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

/** Every wait is a latch or a gate. Only the ratio in the last test depends on timing, and it is generous. */
class ActiveObjectBeanTest {

    @Test
    void fourCallersRestockingAPlainFieldLoseNothingWithNoLock() throws Exception {
        try (ConfigurableApplicationContext context = InventoryApplication.start()) {
            InventoryService inventory = context.getBean(InventoryService.class);
            Thread[] threads = new Thread[4];
            for (int c = 0; c < 4; c++) {
                threads[c] = new Thread(() -> {
                    for (int i = 0; i < 2_000; i++) {
                        inventory.restock(1);
                    }
                });
                threads[c].start();
            }
            for (Thread t : threads) {
                t.join();
            }
            assertEquals(8_000, inventory.available().get(10, TimeUnit.SECONDS));
        }
    }

    @Test
    void theMailboxCountsWhatIsWaitingAndABoundedOneRefuses() throws Exception {
        try (ConfigurableApplicationContext context = InventoryApplication.start()) {
            InventoryService inventory = context.getBean(InventoryService.class);
            Gate gate = new Gate();
            CountDownLatch holding = new CountDownLatch(1);
            CompletableFuture<Integer> stuck = inventory.slowRestock(0, holding, gate);
            assertTrue(holding.await(10, TimeUnit.SECONDS));
            List<CompletableFuture<Integer>> all = new ArrayList<>();
            for (int i = 0; i < 1_000; i++) {
                all.add(inventory.restock(1));
            }
            assertEquals(1_000, InventoryApplication.mailbox(context).getThreadPoolExecutor().getQueue().size());
            gate.open();
            stuck.get(10, TimeUnit.SECONDS);
            for (CompletableFuture<Integer> f : all) {
                f.get(10, TimeUnit.SECONDS);
            }
        }
        try (ConfigurableApplicationContext context = InventoryApplication.start("inventory.mailbox-capacity=3")) {
            InventoryService inventory = context.getBean(InventoryService.class);
            Gate gate = new Gate();
            CountDownLatch holding = new CountDownLatch(1);
            CompletableFuture<Integer> stuck = inventory.slowRestock(0, holding, gate);
            assertTrue(holding.await(10, TimeUnit.SECONDS));
            List<CompletableFuture<Integer>> accepted = new ArrayList<>();
            for (int i = 0; i < 3; i++) {
                accepted.add(inventory.restock(1));
            }
            assertThrows(TaskRejectedException.class, () -> inventory.restock(1));
            gate.open();
            stuck.get(10, TimeUnit.SECONDS);
            for (CompletableFuture<Integer> f : accepted) {
                f.get(10, TimeUnit.SECONDS);
            }
        }
    }

    @Test
    void aCallThroughThisChangesTheFieldOnTheCallersThreadAndAnUpdateIsLost() throws Exception {
        try (ConfigurableApplicationContext context = InventoryApplication.start()) {
            InventoryService inventory = context.getBean(InventoryService.class);
            Gate gate = new Gate();
            CountDownLatch holding = new CountDownLatch(1);
            CompletableFuture<Integer> slow = inventory.slowRestock(10, holding, gate);
            assertTrue(holding.await(10, TimeUnit.SECONDS));
            assertEquals(5, inventory.restockThroughThis(5));
            gate.open();
            slow.get(10, TimeUnit.SECONDS);
            assertEquals(10, inventory.available().get(10, TimeUnit.SECONDS), "5 + 10 should be 15, and one of them was lost");
        }
    }

    @Test
    void aDirectReadSeesThePastAndAReadSentAsAMessageSeesTheRestock() throws Exception {
        try (ConfigurableApplicationContext context = InventoryApplication.start()) {
            InventoryService inventory = context.getBean(InventoryService.class);
            Gate gate = new Gate();
            CountDownLatch holding = new CountDownLatch(1);
            CompletableFuture<Integer> busy = inventory.slowRestock(0, holding, gate);
            assertTrue(holding.await(10, TimeUnit.SECONDS));
            CompletableFuture<Integer> restock = inventory.restock(5);
            assertEquals(0, inventory.peekStock());
            CompletableFuture<Integer> read = inventory.available();
            gate.open();
            busy.get(10, TimeUnit.SECONDS);
            restock.get(10, TimeUnit.SECONDS);
            assertEquals(5, read.get(10, TimeUnit.SECONDS));
        }
    }

    @Test
    void anErrorArrivesLaterWithTheWorkersFramesAndNotTheCallers() {
        try (ConfigurableApplicationContext context = InventoryApplication.start()) {
            CompletionException e = assertThrows(CompletionException.class,
                    () -> context.getBean(InventoryService.class).failWith("feed down").join());
            assertTrue(e.getCause().getMessage().contains("raised on inventory-"), e.getCause().getMessage());
            for (StackTraceElement frame : e.getCause().getStackTrace()) {
                assertFalse(frame.getClassName().contains("ActiveObjectBeanTest"), frame.toString());
            }
        }
    }

    @Test
    void messagesFromOneCallerAreProcessedInTheOrderTheyWereSent() throws Exception {
        try (ConfigurableApplicationContext context = InventoryApplication.start()) {
            InventoryService inventory = context.getBean(InventoryService.class);
            List<CompletableFuture<Integer>> replies = new ArrayList<>();
            for (int i = 0; i < 100; i++) {
                replies.add(inventory.restock(1));
            }
            for (int i = 0; i < 100; i++) {
                assertEquals(i + 1, replies.get(i).get(10, TimeUnit.SECONDS));
            }
        }
    }

    @Test
    void moreCallersDoNotRaiseTheRateWhenTheOneWorkerIsTheBottleneck() throws Exception {
        long one = InventoryApplication.throughput(1, 400, 50_000);
        long four = InventoryApplication.throughput(4, 100, 50_000);
        assertTrue(four < one * 2, "one=" + one + " four=" + four);
    }
}
