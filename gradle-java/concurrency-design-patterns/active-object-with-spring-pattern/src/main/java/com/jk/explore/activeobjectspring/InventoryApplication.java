package com.jk.explore.activeobjectspring;

import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.context.ConfigurableApplicationContext;
import org.springframework.core.task.TaskRejectedException;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.CompletionException;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;

/** Six acts. Every wait is a latch or a gate, never a sleep. */
@SpringBootApplication
public class InventoryApplication {

    public static void main(String[] args) throws Exception {
        System.out.println("ACTIVE OBJECT WITH SPRING — one thread, one mailbox\n");
        actOne();
        actTwo();
        actThree();
        actFour();
        actFive();
        actSix();
    }

    static ConfigurableApplicationContext start(String... properties) {
        return new SpringApplicationBuilder(InventoryApplication.class).properties(properties).run();
    }

    static ThreadPoolTaskExecutor mailbox(ConfigurableApplicationContext context) {
        return context.getBean("inventoryExecutor", ThreadPoolTaskExecutor.class);
    }

    private static void actOne() throws Exception {
        System.out.println("ONE. A bean on a one-thread executor: state with no lock.");
        try (ConfigurableApplicationContext context = start()) {
            InventoryService inventory = context.getBean(InventoryService.class);
            int callers = 4;
            int each = 5_000;
            Thread[] threads = new Thread[callers];
            for (int c = 0; c < callers; c++) {
                threads[c] = new Thread(() -> {
                    for (int i = 0; i < each; i++) {
                        inventory.restock(1);
                    }
                });
                threads[c].start();
            }
            for (Thread t : threads) {
                t.join();
            }
            System.out.println("  " + callers + " callers x " + each + " restocks: stock " + inventory.available().get(10, TimeUnit.SECONDS));
            System.out.println("  the stock field is a plain int: no lock, not volatile. every change ran on the inventory- thread.\n");
        }
    }

    private static void actTwo() throws Exception {
        System.out.println("TWO. The mailbox is the executor's queue, and it has the partner's costs.");
        try (ConfigurableApplicationContext context = start()) {
            InventoryService inventory = context.getBean(InventoryService.class);
            Gate gate = new Gate();
            CountDownLatch holding = new CountDownLatch(1);
            CompletableFuture<Integer> stuck = inventory.slowRestock(0, holding, gate);
            holding.await(10, TimeUnit.SECONDS);
            List<CompletableFuture<Integer>> all = new ArrayList<>();
            for (int i = 0; i < 10_000; i++) {
                all.add(inventory.restock(1));
            }
            System.out.println("  the worker is busy on one slow message. callers send 10000 more.");
            System.out.println("  messages waiting in the mailbox: " + mailbox(context).getThreadPoolExecutor().getQueue().size()
                    + ". nothing refused them.");
            gate.open();
            stuck.get(10, TimeUnit.SECONDS);
            for (CompletableFuture<Integer> f : all) {
                f.get(10, TimeUnit.SECONDS);
            }
        }
        try (ConfigurableApplicationContext context = start("inventory.mailbox-capacity=3")) {
            InventoryService inventory = context.getBean(InventoryService.class);
            Gate gate = new Gate();
            CountDownLatch holding = new CountDownLatch(1);
            CompletableFuture<Integer> stuck = inventory.slowRestock(0, holding, gate);
            holding.await(10, TimeUnit.SECONDS);
            List<CompletableFuture<Integer>> accepted = new ArrayList<>();
            for (int i = 0; i < 3; i++) {
                accepted.add(inventory.restock(1));
            }
            try {
                inventory.restock(1);
            } catch (TaskRejectedException e) {
                System.out.println("  with a mailbox of 3: the fourth message waiting is refused with " + e.getClass().getSimpleName() + ". that is a bound.");
            }
            gate.open();
            stuck.get(10, TimeUnit.SECONDS);
            for (CompletableFuture<Integer> f : accepted) {
                f.get(10, TimeUnit.SECONDS);
            }
            System.out.println();
        }
    }

    private static void actThree() throws Exception {
        System.out.println("THREE. One call that skips the proxy breaks the guarantee.");
        try (ConfigurableApplicationContext context = start()) {
            InventoryService inventory = context.getBean(InventoryService.class);
            Gate gate = new Gate();
            CountDownLatch holding = new CountDownLatch(1);
            CompletableFuture<Integer> slow = inventory.slowRestock(10, holding, gate);
            holding.await(10, TimeUnit.SECONDS);
            int viaThis = inventory.restockThroughThis(5);
            System.out.println("  the worker read the stock (0) and is holding it. a caller adds 5 through this, on its own thread: stock " + viaThis + ".");
            gate.open();
            slow.get(10, TimeUnit.SECONDS);
            System.out.println("  the worker then writes 0 + 10. final stock: " + inventory.available().get(10, TimeUnit.SECONDS) + ", not 15. five items vanished.");
            System.out.println("  with two threads changing a plain field, the lock-free design is gone, and nothing complains.\n");
        }
    }

    private static void actFour() throws Exception {
        System.out.println("FOUR. A read that skips the mailbox sees the past.");
        try (ConfigurableApplicationContext context = start()) {
            InventoryService inventory = context.getBean(InventoryService.class);
            Gate gate = new Gate();
            CountDownLatch holding = new CountDownLatch(1);
            CompletableFuture<Integer> busy = inventory.slowRestock(0, holding, gate);
            holding.await(10, TimeUnit.SECONDS);
            CompletableFuture<Integer> restock = inventory.restock(5);
            System.out.println("  a restock of 5 has been sent, and is waiting its turn behind a slow message.");
            System.out.println("  a getter that reads the field directly, from the caller's thread, says: " + inventory.peekStock() + ".");
            CompletableFuture<Integer> read = inventory.available();
            gate.open();
            busy.get(10, TimeUnit.SECONDS);
            restock.get(10, TimeUnit.SECONDS);
            System.out.println("  a read sent as a message, behind the restock, says: " + read.get(10, TimeUnit.SECONDS) + ".");
            System.out.println("  the direct read raced the worker, and lost. in an active object, reads are messages too.\n");
        }
    }

    private static void actFive() throws Exception {
        System.out.println("FIVE. Errors arrive later, from the worker.");
        try (ConfigurableApplicationContext context = start()) {
            try {
                context.getBean(InventoryService.class).failWith("stock feed unavailable").join();
            } catch (CompletionException e) {
                System.out.println("  cause: " + e.getCause().getMessage());
                boolean callerAppears = false;
                for (StackTraceElement frame : e.getCause().getStackTrace()) {
                    callerAppears |= frame.getMethodName().equals("actFive");
                }
                System.out.println("  the calling method appears nowhere in that trace: " + !callerAppears + ".\n");
            }
        }
    }

    private static void actSix() throws Exception {
        System.out.println("SIX. One worker is a ceiling.");
        long work = 50_000;
        long one = throughput(1, 1_000, work);
        long four = throughput(4, 250, work);
        System.out.println("  every message costs 50 microseconds of work, all on the one inventory- thread.");
        System.out.println("  1 caller:  " + one + " per second");
        System.out.println("  4 callers: " + four + " per second");
        System.out.println("  four times the callers, the same rate: the ceiling is the worker, as in the partner project.");
        System.out.println("  verdict: an @Async bean on a one-thread executor is an active object. route every call, reads included, through the proxy,");
        System.out.println("  and bound the mailbox. where you have met this: a single-thread executor and @Async(\"name\").");
    }

    static long throughput(int callers, int each, long spinNanos) throws Exception {
        try (ConfigurableApplicationContext context = start()) {
            InventoryService inventory = context.getBean(InventoryService.class);
            Gate go = new Gate();
            CompletableFuture<?>[] lasts = new CompletableFuture<?>[callers];
            Thread[] threads = new Thread[callers];
            for (int c = 0; c < callers; c++) {
                int index = c;
                threads[c] = new Thread(() -> {
                    go.awaitOpen();
                    CompletableFuture<Integer> last = null;
                    for (int i = 0; i < each; i++) {
                        last = inventory.restockWithWork(1, spinNanos);
                    }
                    lasts[index] = last;
                });
                threads[c].start();
            }
            long start = System.nanoTime();
            go.open();
            for (Thread t : threads) {
                t.join();
            }
            CompletableFuture.allOf(lasts).get(60, TimeUnit.SECONDS);
            return callers * (long) each * 1_000_000_000L / Math.max(1, System.nanoTime() - start);
        }
    }
}
