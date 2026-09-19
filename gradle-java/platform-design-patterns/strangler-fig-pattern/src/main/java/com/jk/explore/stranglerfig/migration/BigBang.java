package com.jk.explore.stranglerfig.migration;

/**
 * <strong>The big-bang rewrite, on a compressed timeline.</strong> Months of work in
 * parallel with production, a cutover weekend, and a fault on the Monday. The only
 * rollback is the whole thing, so one broken capability takes four working ones
 * back with it. Numbers are a model, stated as such.
 */
public final class BigBang {

    /** Weeks of parallel work before the cutover, and orders the new code served in that time: none. */
    public static final int WEEKS_OF_PARALLEL_WORK = 26;

    public record Outcome(int weeksOfWork, int ordersServedByNewCodeBeforeCutover, int capabilitiesInNewCode,
                          int capabilitiesFaulty, int capabilitiesRolledBack, boolean rollbackWasAllOrNothing) {
    }

    private BigBang() {
    }

    public static Outcome run() {
        int capabilities = 4;
        int faulty = 1; // payment declines large orders, found only under Monday's real traffic
        // there is one switch, so "roll back" can only mean "roll back everything".
        return new Outcome(WEEKS_OF_PARALLEL_WORK, 0, capabilities, faulty, capabilities, true);
    }
}
