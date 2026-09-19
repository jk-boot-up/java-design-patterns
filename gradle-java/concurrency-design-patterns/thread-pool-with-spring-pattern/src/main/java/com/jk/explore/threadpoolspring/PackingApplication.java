package com.jk.explore.threadpoolspring;

import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.context.ConfigurableApplicationContext;
import org.springframework.core.task.TaskRejectedException;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;

/**
 * Six acts. Every wait is a latch or a gate, never a sleep, so every count is the same every run.
 */
@SpringBootApplication
@EnableAsync
public class PackingApplication {

    public static void main(String[] args) throws Exception {
        System.out.println("THREAD POOL WITH SPRING — the executor behind @Async\n");
        actOne();
        actTwo();
        actThree();
        actFour();
        actFive();
        actSix();
    }

    static ConfigurableApplicationContext start(String... properties) {
        return new SpringApplicationBuilder(PackingApplication.class).properties(properties).run();
    }

    static ThreadPoolTaskExecutor pool(ConfigurableApplicationContext context) {
        return context.getBean("applicationTaskExecutor", ThreadPoolTaskExecutor.class);
    }

    private static void actOne() {
        System.out.println("ONE. What Spring Boot gives you when you configure nothing.");
        try (ConfigurableApplicationContext context = start()) {
            ThreadPoolTaskExecutor pool = pool(context);
            System.out.println("  @EnableAsync and no settings. the executor is a ThreadPoolTaskExecutor:");
            System.out.println("  core threads " + pool.getCorePoolSize() + ", max threads " + pool.getMaxPoolSize()
                    + ", queue capacity " + pool.getThreadPoolExecutor().getQueue().remainingCapacity() + ".");
            System.out.println("  eight workers, and a queue with no bound. this is the partner project's unbounded-queue trap, as a default.\n");
        }
    }

    private static void actTwo() throws Exception {
        System.out.println("TWO. @Async moves the work to another thread.");
        try (ConfigurableApplicationContext context = start()) {
            Gate gate = new Gate();
            gate.open();
            String worker = context.getBean(PackingService.class).pack(1, new CountDownLatch(1), gate).get(5, TimeUnit.SECONDS);
            System.out.println("  the caller is thread \"" + Thread.currentThread().getName() + "\". the work ran on \"" + worker + "\".");
            System.out.println("  one annotation replaced the partner's BoundedPackingPool class.\n");
        }
    }

    private static void actThree() throws Exception {
        System.out.println("THREE. The unbounded queue, with the workers busy.");
        try (ConfigurableApplicationContext context = start()) {
            PackingService packing = context.getBean(PackingService.class);
            Gate gate = new Gate();
            List<CompletableFuture<String>> all = new ArrayList<>();
            CountDownLatch eightRunning = new CountDownLatch(8);
            for (int i = 0; i < 8; i++) {
                all.add(packing.pack(i, eightRunning, gate));
            }
            eightRunning.await(10, TimeUnit.SECONDS);
            for (int i = 0; i < 1_000; i++) {
                all.add(packing.pack(100 + i, new CountDownLatch(1), gate));
            }
            System.out.println("  all 8 workers are stuck on a slow step. 1000 more orders arrive.");
            System.out.println("  waiting in the queue: " + pool(context).getThreadPoolExecutor().getQueue().size() + ". rejected: 0. nobody was told.");
            System.out.println("  submitting never blocks and never refuses. the backlog just grows, until it is a heap dump instead of a decision.");
            gate.open();
            for (CompletableFuture<String> f : all) {
                f.get(10, TimeUnit.SECONDS);
            }
            System.out.println();
        }
    }

    private static void actFour() throws Exception {
        System.out.println("FOUR. Bound it, and the refusal is a real exception.");
        try (ConfigurableApplicationContext context = start("spring.task.execution.pool.core-size=2",
                "spring.task.execution.pool.max-size=2", "spring.task.execution.pool.queue-capacity=3")) {
            PackingService packing = context.getBean(PackingService.class);
            Gate gate = new Gate();
            CountDownLatch twoRunning = new CountDownLatch(2);
            List<CompletableFuture<String>> accepted = new ArrayList<>();
            for (int i = 0; i < 2; i++) {
                accepted.add(packing.pack(i, twoRunning, gate));
            }
            twoRunning.await(10, TimeUnit.SECONDS);
            for (int i = 0; i < 3; i++) {
                accepted.add(packing.pack(10 + i, new CountDownLatch(1), gate));
            }
            System.out.println("  three settings: 2 threads, a queue of 3. two orders are running and three are waiting.");
            try {
                packing.pack(99, new CountDownLatch(1), gate);
            } catch (TaskRejectedException e) {
                System.out.println("  the sixth order: " + e.getClass().getSimpleName() + ", thrown to the caller, at once.");
            }
            System.out.println("  that is a decision: the caller learns the pool is full, instead of a queue growing in silence.");
            gate.open();
            for (CompletableFuture<String> f : accepted) {
                f.get(10, TimeUnit.SECONDS);
            }
            System.out.println();
        }
    }

    private static void actFive() throws Exception {
        System.out.println("FIVE. The annotation that does nothing.");
        try (ConfigurableApplicationContext context = start()) {
            String worker = context.getBean(PackingService.class).packThroughThis(1).get(5, TimeUnit.SECONDS);
            System.out.println("  packThroughThis() called pack(), which is @Async, through this. it ran on \"" + worker + "\", the caller's own thread.");
            System.out.println("  @Async works through a proxy, exactly as @Transactional does. a call on this skips it, and nothing complains.\n");
        }
    }

    private static void actSix() throws Exception {
        System.out.println("SIX. Pool starvation: a task that waits for a task on its own pool.");
        try (ConfigurableApplicationContext context = start("spring.task.execution.pool.core-size=1",
                "spring.task.execution.pool.max-size=1", "spring.task.execution.pool.queue-capacity=5")) {
            String outcome = context.getBean(PackingService.class).packAndWaitForALabel().get(10, TimeUnit.SECONDS);
            System.out.println("  one thread. the packing task asks the pool to print a label, and waits for it.");
            System.out.println("  " + outcome);
            System.out.println("  the label task is queued behind the packing task, which is waiting for it. the same deadlock as the partner's act five.");
            System.out.println("  verdict: set the pool explicitly, bound the queue, and never wait on your own pool.");
            System.out.println("  where you have met this: every @Async method, and Spring Boot's applicationTaskExecutor.");
        }
    }
}
