package com.jk.explore.stranglerfig.migration;

import java.util.ArrayList;
import java.util.List;

/**
 * <strong>The failure mode that actually happens: the migration stalls.</strong>
 * A cost model, stated as one. Every unit is arbitrary and only the shape matters:
 * a system that is fully legacy costs 100 a quarter to run, fully new costs 60, and
 * while both are live each pays a fixed price for existing (a second on-call, a
 * second deploy pipeline, keeping data in step) on top of the share of the work it
 * carries. Moving one capability costs 30 of migration effort.
 */
public final class StallModel {

    public static final int LEGACY_ALL = 100;
    public static final int NEW_ALL = 60;
    public static final int RUNNING_BOTH_OVERHEAD = 35;
    public static final int MIGRATION_EFFORT_PER_CAPABILITY = 30;

    public record Quarter(int number, int capabilitiesMoved, int budgetForMigration, int runningCost, int migrationSpend) {

        public int totalCost() {
            return runningCost + migrationSpend;
        }
    }

    private StallModel() {
    }

    /** Running cost with {@code moved} of four capabilities on the new system. */
    public static int runningCost(int moved) {
        if (moved == 0) {
            return LEGACY_ALL;
        }
        if (moved == 4) {
            return NEW_ALL;
        }
        int legacyShare = LEGACY_ALL * (4 - moved) / 4;
        int newShare = NEW_ALL * moved / 4;
        return legacyShare + newShare + RUNNING_BOTH_OVERHEAD;
    }

    /** Six quarters. The budget for migration is cut after the second, when priorities move elsewhere. */
    public static List<Quarter> stalled() {
        int[] budget = {30, 30, 0, 0, 0, 0};
        List<Quarter> quarters = new ArrayList<>();
        int moved = 0;
        for (int q = 0; q < 6; q++) {
            int spend = 0;
            if (budget[q] >= MIGRATION_EFFORT_PER_CAPABILITY && moved < 4) {
                moved++;
                spend = MIGRATION_EFFORT_PER_CAPABILITY;
            }
            quarters.add(new Quarter(q + 1, moved, budget[q], runningCost(moved), spend));
        }
        return quarters;
    }

    /** The same six quarters if the migration is finished: one capability a quarter, then done. */
    public static List<Quarter> finished() {
        List<Quarter> quarters = new ArrayList<>();
        int moved = 0;
        for (int q = 0; q < 6; q++) {
            int spend = 0;
            if (moved < 4) {
                moved++;
                spend = MIGRATION_EFFORT_PER_CAPABILITY;
            }
            quarters.add(new Quarter(q + 1, moved, MIGRATION_EFFORT_PER_CAPABILITY, runningCost(moved), spend));
        }
        return quarters;
    }
}
