package com.jk.explore.activeobject;

import com.jk.explore.activeobject.harness.Gate;
import com.jk.explore.activeobject.pattern.InventoryActiveObject;
import org.junit.jupiter.api.RepeatedTest;
import org.junit.jupiter.api.Test;

import java.util.concurrent.CompletableFuture;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.TimeUnit;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class InventoryActiveObjectTest {

    @RepeatedTest(20)
    void aCallReturnsBeforeItsWorkIsDoneAndCompletesInOrder() throws Exception {
        try (InventoryActiveObject inventory = new InventoryActiveObject(10)) {
            Gate slow = new Gate();
            CountDownLatch started = new CountDownLatch(1);
            CompletableFuture<Integer> imported = inventory.importCorrection(50, () -> {
                started.countDown();
                slow.awaitOpen();
            });
            started.await();
            CompletableFuture<Integer> reserved = inventory.reserve(1);

            assertFalse(reserved.isDone(), "the call returned, but the work has not happened yet");
            slow.open();
            assertEquals(50, imported.get(5, TimeUnit.SECONDS));
            assertEquals(49, reserved.get(5, TimeUnit.SECONDS), "messages run in the order they arrived");
        }
    }

    @RepeatedTest(20)
    void manyCallersNeverLoseAnUpdateWithoutAnyLock() throws Exception {
        try (InventoryActiveObject inventory = new InventoryActiveObject(0)) {
            int callers = 4, each = 5_000;
            Gate start = new Gate();
            Thread[] threads = new Thread[callers];
            for (int c = 0; c < callers; c++) {
                threads[c] = new Thread(() -> {
                    start.awaitOpen();
                    for (int i = 0; i < each; i++) {
                        inventory.restock(1);
                    }
                });
                threads[c].start();
            }
            start.open();
            for (Thread t : threads) {
                t.join(10_000);
            }
            assertEquals(callers * each, inventory.available().get(10, TimeUnit.SECONDS));
        }
    }

    @Test
    void aFailureSurfacesInTheFutureWithTheWorkersFrames() throws Exception {
        try (InventoryActiveObject inventory = new InventoryActiveObject(10)) {
            ExecutionException e = assertThrows(ExecutionException.class,
                    () -> inventory.failWith("feed down").get(5, TimeUnit.SECONDS));
            assertTrue(e.getCause().getMessage().contains("raised on inventory-worker"));
            for (StackTraceElement frame : e.getCause().getStackTrace()) {
                assertFalse(frame.getClassName().contains("InventoryActiveObjectTest"),
                        "the calling test must not appear in the trace: " + frame);
            }
        }
    }

    @Test
    void aFailureDoesNotStopLaterMessages() throws Exception {
        try (InventoryActiveObject inventory = new InventoryActiveObject(10)) {
            inventory.failWith("feed down");
            assertEquals(9, inventory.reserve(1).get(5, TimeUnit.SECONDS));
        }
    }
}
