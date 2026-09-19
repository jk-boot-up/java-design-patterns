package com.jk.explore.threadlocalstorage;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.RepeatedTest;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import static org.junit.jupiter.api.Assertions.*;

class ThreadLocalTest {

    @AfterEach
    void clean() {
        RequestContext.clear();
        InheritedContext.clear();
    }

    @Test
    void theContextIsReadBelowTheDoorWithoutBeingPassed() {
        Audit a = new Audit();
        RequestContext.with("ada", () -> { ThreadLocalDemo.checkout(a); return null; });
        assertEquals(List.of("ada: reserved stock"), a.lines());
        assertNull(RequestContext.customer());
    }

    @Test
    void theContextIsClearedEvenWhenTheWorkThrows() {
        assertThrows(IllegalStateException.class, () -> RequestContext.with("ada", () -> { throw new IllegalStateException(); }));
        assertNull(RequestContext.customer());
    }

    @RepeatedTest(5)
    void twoThreadsSeeTheirOwnValueEvenWhenBothAreSetBeforeEitherReads() throws Exception {
        Audit a = new Audit();
        CountDownLatch both = new CountDownLatch(2);
        Thread[] ts = new Thread[2];
        String[] names = {"ada", "ben"};
        for (int i = 0; i < 2; i++) {
            String who = names[i];
            ts[i] = new Thread(() -> RequestContext.with(who, () -> {
                both.countDown();
                try { both.await(); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
                a.record("x");
                return null;
            }));
            ts[i].start();
        }
        for (Thread t : ts) t.join();
        assertEquals(List.of("ada: x", "ben: x"), a.lines().stream().sorted().toList());
    }

    @Test
    void aReusedThreadLeaksTheLastRequestsCustomerUnlessItIsCleared() throws Exception {
        assertEquals(List.of("ada: reserved stock", "ada: reserved stock"), ThreadLocalDemo.reusedThread(false));
        assertEquals(List.of("ada: reserved stock", "null: reserved stock"), ThreadLocalDemo.reusedThread(true));
    }

    @Test
    void aPoolThreadDoesNotSeeTheSubmittersContext() throws Exception {
        ExecutorService pool = Executors.newSingleThreadExecutor();
        try {
            RequestContext.set("ada");
            assertNull(pool.submit(RequestContext::customer).get());
        } finally {
            pool.shutdown();
        }
    }

    @Test
    void aNewlyCreatedThreadInheritsACopyFromAnInheritableLocal() throws Exception {
        InheritedContext.set("ada");
        String[] seen = new String[1];
        Thread t = new Thread(() -> seen[0] = InheritedContext.customer());
        t.start();
        t.join();
        assertEquals("ada", seen[0]);
    }

    @Test
    void handingTheContextOnByHandWorks() throws Exception {
        ExecutorService pool = Executors.newSingleThreadExecutor();
        try {
            RequestContext.set("ada");
            String mine = RequestContext.customer();
            assertEquals("ada", pool.submit(() -> RequestContext.with(mine, RequestContext::customer)).get());
        } finally {
            pool.shutdown();
        }
    }

    @Test
    void codeThatReadsTheContextWithNoneSetLogsNull() {
        Audit a = new Audit();
        a.record("x");
        assertEquals(List.of("null: x"), a.lines());
    }
}
