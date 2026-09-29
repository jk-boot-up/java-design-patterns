package com.jk.explore.scheduler;

import java.util.ArrayList;
import java.util.List;

/**
 * The five acts: a fair lock, an express-first scheduler, a different policy, no job waits for ever, and the bill.
 */
public final class SchedulerDemo {

    static final List<Object[]> MIXED = List.of(
            new Object[] {"STD-1", false, 4}, new Object[] {"STD-2", false, 1}, new Object[] {"STD-3", false, 2},
            new Object[] {"EXP-1", true, 3}, new Object[] {"EXP-2", true, 1}, new Object[] {"EXP-3", true, 2});

    static final List<Object[]> EXPRESS_RUSH = List.of(
            new Object[] {"STD-1", false, 1}, new Object[] {"EXP-1", true, 1}, new Object[] {"EXP-2", true, 1},
            new Object[] {"EXP-3", true, 1}, new Object[] {"EXP-4", true, 1}, new Object[] {"EXP-5", true, 1});

    public static void main(String[] args) throws Exception {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() throws Exception {
        List<String> out = new ArrayList<>();
        out.add("One label printer; a bulk job is printing while six stations send theirs.");
        out.add("");

        out.add("ONE. A fair lock: first come, first served.");
        out.add("  printed: " + Printer.run(Printer.fairLock(), MIXED));
        out.add("  the three express orders waited behind every standard one");

        out.add("");
        out.add("TWO. A scheduler with an express-first policy.");
        out.add("  printed: " + Printer.run(Printer.scheduler(new Scheduler(Scheduler.EXPRESS_FIRST)), MIXED));
        out.add("  every station asked for its turn; the policy chose whose turn came next");

        out.add("");
        out.add("THREE. The policy is replaceable: smallest job first.");
        out.add("  printed: " + Printer.run(Printer.scheduler(new Scheduler(Scheduler.SMALLEST_FIRST)), MIXED));
        out.add("  one comparator changed; the stations and the printer did not");

        out.add("");
        out.add("FOUR. Nobody waits for ever.");
        out.add("  express only, with a rush of express: "
                + Printer.run(Printer.scheduler(new Scheduler(Scheduler.EXPRESS_FIRST)), EXPRESS_RUSH));
        out.add("  promote a job passed over 3 times:    "
                + Printer.run(Printer.scheduler(new Scheduler(Scheduler.EXPRESS_FIRST, 3)), EXPRESS_RUSH));

        out.add("");
        out.add("FIVE. The bill: someone has to decide, every time.");
        out.add("  every job takes the scheduler's lock, joins its list, and is woken to check whether it is next");
        out.add("  and every priority rule needs a guard against starving the others");
        return out;
    }

    private SchedulerDemo() {
    }
}
