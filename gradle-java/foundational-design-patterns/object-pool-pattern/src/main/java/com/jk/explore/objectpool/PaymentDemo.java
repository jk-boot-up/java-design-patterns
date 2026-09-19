package com.jk.explore.objectpool;

import com.jk.explore.objectpool.bench.SmallObjectBenchmark;
import com.jk.explore.objectpool.domain.PaymentConnection;
import com.jk.explore.objectpool.naive.ConnectionPerPayment;
import com.jk.explore.objectpool.pattern.ConnectionPool;

import java.util.ArrayList;
import java.util.List;

/**
 * Six acts. The handshake is a stand-in for a real network handshake and takes
 * 200 milliseconds. Timings are real and vary by machine; counts do not.
 */
public final class PaymentDemo {

    static final long HANDSHAKE_MILLIS = 200;
    static final int PAYMENTS = 10;

    public static void main(String[] args) throws InterruptedException {
        System.out.println("OBJECT POOL — expensive to make, cheap to borrow\n");

        actOne();
        actTwo();
        actThree();
        actFour();
        actFive();
        actSix();
    }

    private static void actOne() {
        System.out.println("ONE. A new connection for every payment.");
        PaymentConnection.resetCounter();
        ConnectionPerPayment naive = new ConnectionPerPayment(HANDSHAKE_MILLIS);
        long start = System.nanoTime();
        for (int i = 0; i < PAYMENTS; i++) {
            naive.pay("customer " + i, 1_000);
        }
        long millis = (System.nanoTime() - start) / 1_000_000;
        System.out.println("  " + PAYMENTS + " payments: " + PaymentConnection.openedSoFar() + " connections opened, " + millis + "ms.");
        System.out.println("  every payment paid a " + HANDSHAKE_MILLIS + "ms handshake. simple, correct, and slow.\n");
    }

    private static void actTwo() throws InterruptedException {
        System.out.println("TWO. A pool of two connections, borrowed and returned.");
        PaymentConnection.resetCounter();
        long start = System.nanoTime();
        ConnectionPool pool = new ConnectionPool(2, HANDSHAKE_MILLIS, true);
        for (int i = 0; i < PAYMENTS; i++) {
            PaymentConnection c = pool.borrow();
            c.charge("customer " + i, 1_000);
            pool.giveBack(c);
        }
        long millis = (System.nanoTime() - start) / 1_000_000;
        System.out.println("  " + PAYMENTS + " payments: " + PaymentConnection.openedSoFar() + " connections opened, " + millis + "ms, including opening the pool.");
        System.out.println("  this is the right use of the pattern: the thing pooled is expensive outside the JVM.\n");
    }

    private static void actThree() {
        System.out.println("THREE. The bill: pooling a small object is slower than allocating it.");
        SmallObjectBenchmark.Result r = SmallObjectBenchmark.run();
        System.out.println("  a three-field object, " + SmallObjectBenchmark.OPERATIONS + " operations, median of "
                + SmallObjectBenchmark.MEASURED_ROUNDS + " rounds after " + SmallObjectBenchmark.WARMUP_ROUNDS + " warm-up rounds:");
        System.out.printf("  allocating (the JIT may remove it entirely): %.2f ns per operation%n", r.allocateNanosPerOp());
        System.out.printf("  allocating (forced onto the heap):           %.2f ns per operation%n", r.allocateEscapingNanosPerOp());
        System.out.printf("  borrowing from a pool:                       %.2f ns per operation%n", r.poolNanosPerOp());
        System.out.printf("  the pool is %.1f times slower than real allocation.%n", r.poolIsSlowerThanEscapingAllocationBy());
        System.out.println("  objects created: " + SmallObjectBenchmark.objectsCreatedByAllocating(SmallObjectBenchmark.OPERATIONS)
                + " by allocating, " + SmallObjectBenchmark.objectsCreatedByPooling() + " by pooling. the pool wins on that count and loses on time.");
        System.out.println("  why: the pool adds a lock and moves objects through shared memory, and the JVM's allocator is a pointer bump.");
        System.out.println("  timings vary by machine. the direction is the claim, and the method is in the README.\n");
    }

    private static void actFour() throws InterruptedException {
        System.out.println("FOUR. The bill: a returned object carries its old state.");
        ConnectionPool careless = new ConnectionPool(1, 0, false);
        PaymentConnection first = careless.borrow();
        first.charge("Ada Lovelace", 5_000);
        careless.giveBack(first);
        PaymentConnection second = careless.borrow();
        System.out.println("  Grace borrows the connection Ada just returned.");
        System.out.println("  the connection says its last card holder was: " + second.lastCardHolder());
        System.out.println("  a security bug, not a performance one, and the one that happens in the field.");
        ConnectionPool safe = new ConnectionPool(1, 0, true);
        PaymentConnection a = safe.borrow();
        a.charge("Ada Lovelace", 5_000);
        safe.giveBack(a);
        System.out.println("  with a reset on return: " + safe.borrow().lastCardHolder() + ". every pool needs one.\n");
    }

    private static void actFive() throws InterruptedException {
        System.out.println("FIVE. The bill: a leaked object is never returned.");
        ConnectionPool pool = new ConnectionPool(2, 0, true);
        pool.borrow();
        pool.borrow();
        System.out.println("  two borrowers take both connections and never give them back.");
        long start = System.nanoTime();
        PaymentConnection third = pool.borrow(300);
        long millis = (System.nanoTime() - start) / 1_000_000;
        System.out.println("  a third payment waited " + millis + "ms and got: " + (third == null ? "nothing (rescued by a timeout)" : "a connection"));
        System.out.println("  without the timeout it would wait forever. the application hangs. worse than a slow start.\n");
    }

    private static void actSix() throws InterruptedException {
        System.out.println("SIX. The bill: sizing is a guess, and both directions cost.");
        System.out.println("  four payments at the same time, each needing 50ms of work on a connection:");
        System.out.println("  pool of 1:  " + timeFourPayments(1) + "ms (they queue)");
        System.out.println("  pool of 4:  " + timeFourPayments(4) + "ms");
        PaymentConnection.resetCounter();
        new ConnectionPool(50, 0, true);
        System.out.println("  pool of 50: " + PaymentConnection.openedSoFar() + " connections opened, and 46 sit idle, held open, for four payments.");
        System.out.println("  the verdict: pool what is expensive outside the JVM: connections, threads, native handles. nothing else.");
        System.out.println("  a thread pool is the same idea, and the pattern's other unambiguously correct use.");
    }

    private static long timeFourPayments(int poolSize) throws InterruptedException {
        ConnectionPool pool = new ConnectionPool(poolSize, 0, true);
        List<Thread> threads = new ArrayList<>();
        long start = System.nanoTime();
        for (int i = 0; i < 4; i++) {
            Thread t = new Thread(() -> {
                try {
                    PaymentConnection c = pool.borrow();
                    Thread.sleep(50);
                    pool.giveBack(c);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
            threads.add(t);
            t.start();
        }
        for (Thread t : threads) {
            t.join();
        }
        return (System.nanoTime() - start) / 1_000_000;
    }
}
