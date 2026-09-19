package com.jk.explore.loadleveling;

public class LoadLevelingDemo {

    static final int CAPACITY = 10;

    public static void main(String[] args) {
        one();
        two();
        three();
        four();
        five();
        six();
    }

    private static void one() {
        System.out.println("ONE. A burst, straight to the worker.");
        Result r = Sim.direct(Sim.burst(100), CAPACITY, 20);
        System.out.println("  100 orders arrive at once. the order service handles " + CAPACITY + " a tick. processed: " + r.processed() + ", refused: " + r.rejected() + ".");
        System.out.println("  ninety customers were told to try again, on the busiest moment the shop had.");
    }

    private static void two() {
        System.out.println("TWO. A queue in between.");
        Result r = Sim.queued(Sim.burst(100), CAPACITY, 0, 20, -1);
        System.out.println("  the same 100 orders. processed: " + r.processed() + ", refused: " + r.rejected() + ". the deepest the queue got: " + r.maxDepth() + ".");
        System.out.println("  the worker never did more than " + CAPACITY + " a tick. the burst was spread over " + (100 / CAPACITY) + " ticks.");
    }

    private static void three() {
        System.out.println("THREE. What the queue costs: waiting.");
        Result r = Sim.queued(Sim.burst(100), CAPACITY, 0, 20, -1);
        System.out.println("  the first order waited 0 ticks. the last waited " + r.maxWaitTicks() + ". on average: " + r.averageWaitTicks() + ".");
        System.out.println("  no order was lost, and none was fast except the first ten.");
    }

    private static void four() {
        System.out.println("FOUR. A queue with no end, and one with a limit.");
        Result open = Sim.queued(Sim.steady(15), CAPACITY, 0, 100, -1);
        System.out.println("  orders arrive at 15 a tick and the worker does 10, for 100 ticks. an unbounded queue: " + open.leftInQueue() + " orders waiting, and still growing.");
        Result bounded = Sim.queued(Sim.steady(15), CAPACITY, 50, 100, -1);
        System.out.println("  a queue limited to 50: " + bounded.leftInQueue() + " waiting, " + bounded.rejected() + " refused, longest wait " + bounded.maxWaitTicks() + " ticks.");
        System.out.println("  a queue does not fix a worker that is too slow. it hides it, until the limit says so.");
    }

    private static void five() {
        System.out.println("FIVE. Size the worker for the average, not the peak.");
        Result slow = Sim.queued(Sim.burst(100), CAPACITY, 0, 40, -1);
        Result fast = Sim.queued(Sim.burst(100), 2 * CAPACITY, 0, 40, -1);
        System.out.println("  a worker of " + CAPACITY + " a tick clears the burst with a longest wait of " + slow.maxWaitTicks() + ". a worker of " + 2 * CAPACITY + " clears it with a longest wait of " + fast.maxWaitTicks() + ".");
        System.out.println("  to serve a peak of 100 at once with no queue you would need a worker of 100, idle almost all day.");
    }

    private static void six() {
        System.out.println("SIX. The bill: an in-memory queue forgets.");
        Result r = Sim.queued(Sim.burst(100), CAPACITY, 0, 20, 3);
        System.out.println("  the process holding the queue stops at tick 3, with the queue in memory. processed: " + r.processed() + ", lost: " + r.lost() + ".");
        System.out.println("  " + r.lost() + " customers were told their order was accepted, and it never happened.");
        System.out.println("  a queue that must not lose orders has to be kept somewhere that survives.");
    }
}
