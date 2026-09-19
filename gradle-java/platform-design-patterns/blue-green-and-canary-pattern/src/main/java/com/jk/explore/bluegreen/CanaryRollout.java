package com.jk.explore.bluegreen;

import java.util.List;

/** Grows the new release's share in steps, and stops if it is failing too often. */
public class CanaryRollout {

    private final Router router;
    private final int maxFailurePercent;
    private int stepsDone;
    private boolean halted;
    private int lastFailurePercent;

    public CanaryRollout(Router router, int maxFailurePercent) {
        this.router = router;
        this.maxFailurePercent = maxFailurePercent;
    }

    public void run(List<Integer> steps, int requestsPerStep) {
        for (int percent : steps) {
            router.setGreenPercent(percent);
            router.green().resetCounts();
            for (int seq = 0; seq < requestsPerStep; seq++) {
                router.route(seq, Router.orderCents(seq));
            }
            stepsDone++;
            int served = router.green().served();
            lastFailurePercent = served == 0 ? 0 : router.green().failed() * 100 / served;
            if (lastFailurePercent > maxFailurePercent) {
                router.setGreenPercent(0);
                halted = true;
                return;
            }
        }
    }

    public boolean halted() {
        return halted;
    }

    public int stepsDone() {
        return stepsDone;
    }

    public int lastFailurePercent() {
        return lastFailurePercent;
    }
}
