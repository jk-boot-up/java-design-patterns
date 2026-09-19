package com.jk.explore.leaderelection;

import java.util.Optional;

/** One copy of the service. Each minute it asks for the lease, and if it holds it, sends the report. */
public class Node {

    private final String name;
    private final LeaseStore store;
    private final ReportSink sink;
    private final long ttl;
    private boolean alive = true;
    private Lease believedLease;

    public Node(String name, LeaseStore store, ReportSink sink, long ttl) {
        this.name = name;
        this.store = store;
        this.sink = sink;
        this.ttl = ttl;
    }

    public String name() {
        return name;
    }

    public void die() {
        alive = false;
    }

    /** Asks for the lease, and remembers what it was told. */
    public void tryToLead() {
        if (!alive) {
            return;
        }
        Optional<Lease> got = store.acquireOrRenew(name, ttl);
        believedLease = got.orElse(null);
    }

    /** Does the job if this node believes it leads. It does not check again: it acts on what it last heard. */
    public boolean sendReportIfLeader() {
        if (!alive || believedLease == null) {
            return false;
        }
        sink.write(believedLease.token(), name);
        return true;
    }

    /** A node that is not asked to lead but sends anyway, as when nothing coordinates the copies. */
    public void sendReportAlways() {
        if (alive) {
            sink.write(0, name);
        }
    }
}
