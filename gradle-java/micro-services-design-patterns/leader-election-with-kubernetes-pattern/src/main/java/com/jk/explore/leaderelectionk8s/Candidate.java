package com.jk.explore.leaderelectionk8s;

import io.fabric8.kubernetes.client.KubernetesClient;
import io.fabric8.kubernetes.client.extended.leaderelection.LeaderCallbacks;
import io.fabric8.kubernetes.client.extended.leaderelection.LeaderElectionConfigBuilder;
import io.fabric8.kubernetes.client.extended.leaderelection.resourcelock.LeaseLock;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.nio.file.Path;
import java.time.Duration;
import java.util.concurrent.CompletableFuture;

/**
 * One copy of the shop's reporting service, running as its own Java process.
 *
 * <p>It connects to the Kubernetes API server and, unless told not to, joins an election run
 * by Fabric8's LeaderElector on a Lease object. It reports what happens to it as one line
 * on standard output, and takes orders as one line on standard input:
 *
 * <pre>
 *   out: READY                 connected
 *   out: LEADING token         this copy now holds the lease; the token is the lease's
 *                              count of holder changes at that moment
 *   out: NEW_LEADER name       the elector saw a different name in the lease
 *   out: STOPPED               the elector says this copy no longer leads
 *   out: CHECKED true|false    answer to "report": does this copy believe it leads?
 *   out: SEND token            this copy sends the nightly sales report
 *
 *   in:  report                check, and send the report if this copy believes it leads
 *   in:  report-slowly         check, and send only when "go" arrives (the report takes a while)
 *   in:  go                    finish the slow report
 *   in:  rejoin                start a new elector, after the old one has given up
 * </pre>
 */
public final class Candidate {

    /** How long a lease lasts without renewal before another copy may take it. */
    public static final Duration LEASE = Duration.ofSeconds(5);
    /** How long the holder keeps trying to renew before it gives up leading. */
    public static final Duration RENEW_DEADLINE = Duration.ofSeconds(4);
    /** How often the holder renews, and how often the others ask. */
    public static final Duration RETRY = Duration.ofSeconds(1);

    private final String name;
    private final String leaseName;
    private final KubernetesClient client;
    private final BufferedReader in = new BufferedReader(new InputStreamReader(System.in, StandardCharsets.UTF_8));
    private volatile boolean leading;
    private volatile int token = -1;
    private volatile CompletableFuture<?> election;

    private Candidate(String name, String leaseName, KubernetesClient client) {
        this.name = name;
        this.leaseName = leaseName;
        this.client = client;
    }

    /** Arguments: name, kubeconfig path, lease name, and "elect" or "no-election". */
    public static void main(String[] args) throws IOException {
        Candidate me = new Candidate(args[0], args[2], Cluster.connect(Path.of(args[1])));
        boolean elect = "elect".equals(args[3]);
        // A clean shutdown cancels the election, and the elector then hands the lease back.
        Runtime.getRuntime().addShutdownHook(new Thread(me::shutDown));
        say("READY");
        if (elect) {
            me.joinElection();
        }
        String line;
        while ((line = me.in.readLine()) != null) {
            switch (line) {
                case "report" -> me.report(elect, false);
                case "report-slowly" -> me.report(elect, true);
                case "rejoin" -> me.joinElection();
                default -> { }
            }
        }
        // The demo that started this copy has gone. Exit, which runs the shutdown hook.
        System.exit(0);
    }

    private void joinElection() {
        election = client.leaderElector()
                .withConfig(new LeaderElectionConfigBuilder()
                        .withName("nightly-sales-report")
                        .withLock(new LeaseLock(LeaseView.NAMESPACE, leaseName, name))
                        .withLeaseDuration(LEASE)
                        .withRenewDeadline(RENEW_DEADLINE)
                        .withRetryPeriod(RETRY)
                        .withReleaseOnCancel(true)
                        .withLeaderCallbacks(new LeaderCallbacks(this::startedLeading, this::stoppedLeading,
                                leader -> say("NEW_LEADER " + leader)))
                        .build())
                .build()
                .start();
    }

    private void startedLeading() {
        // The token is the lease's own count of how many times the holder has changed.
        // It only ever goes up, so a later leader always carries a bigger one.
        token = LeaseView.read(client, leaseName).map(LeaseView::transitions).orElse(0);
        leading = true;
        say("LEADING " + token);
    }

    private void stoppedLeading() {
        leading = false;
        say("STOPPED");
    }

    /**
     * The nightly sales report. The copy checks whether it leads, and then sends. When the
     * report is slow, those are two moments, and anything can happen between them.
     */
    private void report(boolean elect, boolean slowly) throws IOException {
        if (!elect) {
            say("SEND -1");
            return;
        }
        boolean believesItLeads = leading;
        int myToken = token;
        say("CHECKED " + believesItLeads);
        if (!believesItLeads) {
            return;
        }
        if (slowly) {
            String line;
            while ((line = in.readLine()) != null && !"go".equals(line)) {
                // wait for the report to be finished
            }
        }
        say("SEND " + myToken);
    }

    private void shutDown() {
        CompletableFuture<?> running = election;
        if (running != null) {
            running.cancel(true);
        }
        client.close();
    }

    private static synchronized void say(String line) {
        System.out.println(line);
        System.out.flush();
    }
}
