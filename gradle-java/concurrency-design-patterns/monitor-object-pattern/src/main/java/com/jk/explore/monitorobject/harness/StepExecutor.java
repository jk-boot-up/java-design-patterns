package com.jk.explore.monitorobject.harness;

import java.util.ArrayDeque;
import java.util.Deque;
import java.util.concurrent.Executor;

/**
 * <strong>Harness piece three: an executor with a manual crank.</strong> A
 * task submitted here does not run on a worker thread the moment it
 * arrives — it is queued, and runs only when something calls
 * {@link #runNext()}, on whichever thread makes that call.
 *
 * <p>This is how a test asserts on state <em>between</em> two queued tasks
 * without a real thread pool racing ahead of the assertions. It is not a
 * substitute for a real pool — nothing here runs concurrently with
 * anything else — it is a deterministic stand-in for one, for the tests
 * that need to see one task's effect before the next task starts.
 */
public final class StepExecutor implements Executor {

    private final Deque<Runnable> queued = new ArrayDeque<>();

    @Override
    public void execute(Runnable task) {
        queued.addLast(task);
    }

    /** Runs the oldest queued task, on the calling thread. Returns false if nothing was queued. */
    public boolean runNext() {
        Runnable task = queued.pollFirst();
        if (task == null) {
            return false;
        }
        task.run();
        return true;
    }

    /** Runs every task currently queued, including any a task adds while running. */
    public int runAll() {
        int ran = 0;
        while (runNext()) {
            ran++;
        }
        return ran;
    }

    public int pending() {
        return queued.size();
    }
}
