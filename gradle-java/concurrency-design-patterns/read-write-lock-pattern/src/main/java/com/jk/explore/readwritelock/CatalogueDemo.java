package com.jk.explore.readwritelock;

import com.jk.explore.readwritelock.domain.Price;
import com.jk.explore.readwritelock.harness.Gate;
import com.jk.explore.readwritelock.naive.SingleLockCatalogue;
import com.jk.explore.readwritelock.naive.UnsynchronizedCatalogue;
import com.jk.explore.readwritelock.pattern.ReadWriteCatalogue;
import com.jk.explore.readwritelock.pattern.SnapshotCatalogue;
import com.jk.explore.readwritelock.pattern.UpgradeDeadlock;
import com.jk.explore.readwritelock.pattern.WriterBarging;

import java.math.BigDecimal;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.locks.ReentrantReadWriteLock;
import java.util.function.Supplier;

/**
 * Six acts. No act anywhere calls {@code Thread.sleep} to wait for another
 * thread — throughput timings in acts two, three and six measure real,
 * unpadded work, which is the entire point of measuring them.
 */
public final class CatalogueDemo {

    private static final Price ORIGINAL = new Price(new BigDecimal("49.99"), "GBP");
    private static final Price UPDATED = new Price(new BigDecimal("54.99"), "EUR");

    private static final int READERS = 8;
    private static final int READS_PER_READER = 50_000;

    public static void main(String[] args) throws InterruptedException {
        System.out.println("READ-WRITE LOCK — a thousand readers, one price change\n");

        actOne();
        actTwo();
        actThree();
        actFour();
        actFive();
        actSix();
    }

    private static void actOne() throws InterruptedException {
        System.out.println("ONE. No lock at all — the torn read.");
        Gate midWrite = new Gate();
        CountDownLatch amountSet = new CountDownLatch(1);
        UnsynchronizedCatalogue catalogue = new UnsynchronizedCatalogue(ORIGINAL, () -> {
            amountSet.countDown();
            midWrite.awaitOpen();
        });

        Thread writer = new Thread(() -> catalogue.write(UPDATED));
        writer.start();

        // Deterministic: the new amount is set before this latch can fire,
        // and the writer cannot set the new currency until this method
        // opens the gate below -- so the read below is proven to land in
        // the gap between the two writes, not guessed at.
        amountSet.await();
        Price torn = catalogue.read();
        midWrite.open();
        writer.join();

        System.out.println("  read mid-update: " + torn.amount() + " " + torn.currency());
        System.out.println("  never a true price: the new amount with the old currency.");
        System.out.println();
    }

    private static void actTwo() throws InterruptedException {
        System.out.println("TWO. One mutual-exclusion lock — correct, but readers queue too.");
        SingleLockCatalogue catalogue = new SingleLockCatalogue(ORIGINAL);
        long elapsed = measureThroughput(catalogue::read);
        System.out.printf("  %d readers x %,d reads each: %.0fms%n", READERS, READS_PER_READER,
                elapsed / 1_000_000.0);
        System.out.println("  every reader queued behind every other reader -- two readers");
        System.out.println("  can never conflict, and this lock cannot tell them apart.");
        System.out.println();
    }

    private static void actThree() throws InterruptedException {
        System.out.println("THREE. The pattern — many readers together, a writer alone.");
        ReadWriteCatalogue catalogue = new ReadWriteCatalogue(ORIGINAL);
        long elapsed = measureThroughput(catalogue::read);
        System.out.printf("  %d readers x %,d reads each: %.0fms%n", READERS, READS_PER_READER,
                elapsed / 1_000_000.0);
        System.out.println("  no reader ever waited on another reader -- and for a read this");
        System.out.println("  cheap, that freedom costs more than it saves. See act six.");
        System.out.println();
    }

    private static void actFour() throws InterruptedException {
        System.out.println("FOUR. The mechanism behind writer starvation.");
        ReentrantReadWriteLock lock = new ReentrantReadWriteLock();
        WriterBarging.Outcome outcome = WriterBarging.demonstrate(lock);
        System.out.println("  writer genuinely queued, waiting: " + outcome.writerWasQueued());
        System.out.println("  a second reader's tryLock() barged past it anyway: " + outcome.secondReaderBarged());
        System.out.println("  documented behaviour, not a fluke -- do this continuously and a");
        System.out.println("  writer can wait far longer than its own work would ever justify.");
        System.out.println();
    }

    private static void actFive() throws InterruptedException {
        System.out.println("FIVE. Upgrading a read lock to a write lock deadlocks.");
        ReentrantReadWriteLock lock = new ReentrantReadWriteLock();
        UpgradeDeadlock.Outcome outcome = UpgradeDeadlock.attemptUpgrade(lock, 200);
        System.out.println("  same thread, holding the read lock, requests the write lock:");
        System.out.println("  deadlocked: " + outcome.deadlocked() + ", rescued after " + outcome.waitedMillis()
                + "ms by a demonstration timeout");
        System.out.println("  left alone, this thread waits on itself forever.");
        System.out.println();
    }

    private static void actSix() throws InterruptedException {
        System.out.println("SIX. When the lock loses.");
        SingleLockCatalogue single = new SingleLockCatalogue(ORIGINAL);
        long singleElapsed = measureThroughput(single::read);

        ReadWriteCatalogue locked = new ReadWriteCatalogue(ORIGINAL);
        long lockedElapsed = measureThroughput(locked::read);

        SnapshotCatalogue snapshot = new SnapshotCatalogue(ORIGINAL);
        long snapshotElapsed = measureThroughput(snapshot::read);

        System.out.printf("  single mutex:      %.0fms%n", singleElapsed / 1_000_000.0);
        System.out.printf("  read-write lock:    %.0fms%n", lockedElapsed / 1_000_000.0);
        System.out.printf("  immutable snapshot: %.0fms%n", snapshotElapsed / 1_000_000.0);
        System.out.println("  the lock advertised for readers is the slowest of the three --");
        System.out.println("  managing 'many readers may proceed together' costs real");
        System.out.println("  synchronization of its own. For a price this cheap to copy,");
        System.out.println("  the snapshot needs no lock, and no readers to coordinate at all.");
    }

    private static long measureThroughput(Supplier<Price> read) throws InterruptedException {
        CountDownLatch ready = new CountDownLatch(READERS);
        Gate starter = new Gate();
        Thread[] threads = new Thread[READERS];
        for (int i = 0; i < READERS; i++) {
            threads[i] = new Thread(() -> {
                ready.countDown();
                starter.awaitOpen();
                for (int j = 0; j < READS_PER_READER; j++) {
                    read.get();
                }
            });
            threads[i].start();
        }
        ready.await();
        long start = System.nanoTime();
        starter.open();
        for (Thread t : threads) {
            t.join();
        }
        return System.nanoTime() - start;
    }
}
