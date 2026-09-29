package com.jk.explore.asyncreply;

/**
 * The slow work: adding up every order into a sales report, which takes 6 seconds.
 */
public final class ReportBuilder {

    public static final long WORK_MS = 6000;

    private int runs;

    /** Called once per job; the report itself is always the same, so the demo can compare. */
    public String build() {
        runs++;
        return "412 orders, £18240.50";
    }

    public int runs() {
        return runs;
    }
}
