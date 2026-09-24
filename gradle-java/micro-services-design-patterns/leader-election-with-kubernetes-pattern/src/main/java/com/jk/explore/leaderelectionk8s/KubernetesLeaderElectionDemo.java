package com.jk.explore.leaderelectionk8s;

import io.fabric8.kubernetes.api.model.coordination.v1.Lease;
import io.fabric8.kubernetes.client.KubernetesClient;
import io.fabric8.kubernetes.client.KubernetesClientException;
import java.nio.file.Path;
import java.time.Duration;
import java.time.ZonedDateTime;
import java.util.List;
import java.util.Set;

/**
 * Six acts against a real Kubernetes API server, in a kind cluster that this program creates
 * at the start and deletes at the end.
 *
 * <p>The shop runs three copies of its reporting service, A, B and C, as three separate Java
 * processes. Each night exactly one of them must send the store manager the sales report.
 * The copies decide which one by holding a Kubernetes Lease through Fabric8's LeaderElector.
 */
public class KubernetesLeaderElectionDemo {

    static final String LEASE = "nightly-sales-report";
    static final long LEASE_SECONDS = Candidate.LEASE.toSeconds();
    static final long RETRY_SECONDS = Candidate.RETRY.toSeconds();

    public static void main(String[] args) {
        if (!Cluster.containerRuntimeAvailable()) {
            System.out.println(Cluster.NO_RUNTIME_ADVICE);
            return;
        }
        if (!Cluster.kindAvailable()) {
            System.out.println(Cluster.NO_KIND_ADVICE);
            return;
        }
        try (Cluster cluster = new Cluster()) {
            try {
                cluster.create();
            } catch (RuntimeException e) {
                System.out.println(Cluster.WOULD_NOT_START_ADVICE);
                return;
            }
            one(cluster.kubeconfig());
            two(cluster);
            three(cluster);
            four(cluster);
            List<ServiceCopy> survivors = five(cluster);
            try {
                six(cluster, survivors.get(0), survivors.get(1));
            } finally {
                survivors.forEach(ServiceCopy::close);
            }
        }
    }

    /** Starts copies one at a time, each after the one before it has connected. */
    private static List<ServiceCopy> startCopies(Path kubeconfig, boolean elect, Inbox inbox, String... names) {
        List<ServiceCopy> copies = new java.util.ArrayList<>();
        for (String name : names) {
            ServiceCopy copy = ServiceCopy.start(name, kubeconfig, LEASE, elect, inbox);
            copy.awaitSaying("READY");
            copies.add(copy);
        }
        return copies;
    }

    /** A leads, and every other copy has been told so by its own elector. */
    private static List<ServiceCopy> electA(Cluster cluster, Inbox inbox, String... others) {
        LeaseView.delete(cluster.client(), LEASE);
        ServiceCopy a = startCopies(cluster.kubeconfig(), true, inbox, "A").get(0);
        a.awaitSaying("LEADING 0");
        List<ServiceCopy> copies = new java.util.ArrayList<>(List.of(a));
        for (ServiceCopy other : startCopies(cluster.kubeconfig(), true, inbox, others)) {
            other.awaitSaying("NEW_LEADER A");
            copies.add(other);
        }
        return copies;
    }

    private static void one(Path kubeconfig) {
        System.out.println("ONE. Three copies, nobody in charge.");
        Inbox inbox = new Inbox(false);
        List<ServiceCopy> copies = startCopies(kubeconfig, false, inbox, "A", "B", "C");
        try {
            for (ServiceCopy copy : copies) {
                int before = inbox.received();
                copy.tell("report");
                Poll.until(copy.name() + " to send", () -> inbox.received() == before + 1);
            }
            System.out.println("  three copies of the reporting service run as " + copies.size() + " separate processes. none of them asks who is in charge.");
            System.out.println("  the nightly sales report is sent by every copy: " + inbox.senders() + ".");
            System.out.println("  the manager receives it " + inbox.received() + " times.");
        } finally {
            copies.forEach(ServiceCopy::close);
        }
    }

    private static void two(Cluster cluster) {
        System.out.println("TWO. One holds the lease.");
        Inbox inbox = new Inbox(false);
        List<ServiceCopy> copies = electA(cluster, inbox, "B", "C");
        try {
            LeaseView lease = LeaseView.read(cluster.client(), LEASE).orElseThrow();
            System.out.println("  A asks the API server first and is written into the lease. it says: holder " + lease.holder()
                    + ", lasts " + lease.durationSeconds() + " seconds, holder changes " + lease.transitions() + ".");
            System.out.println("  A renews it every " + RETRY_SECONDS + " second. B and C ask as often, and each is told the leader is "
                    + copies.get(1).saidAfter("NEW_LEADER ") + ".");
            for (ServiceCopy copy : copies) {
                copy.tell("report");
                copy.awaitSayingSomething("CHECKED ");
            }
            Poll.until("A's report to arrive", () -> inbox.received() == 1);
            System.out.println("  all three are asked to send the report. the report was sent by: " + inbox.senders() + ".");
        } finally {
            copies.forEach(ServiceCopy::close);
        }
        String conflict = twoWritesFromOneVersion(cluster.client());
        System.out.println("  two writes to the lease, both based on the same version of it: the first is accepted, the second " + conflict + ".");
        System.out.println("  that refusal is the only rule the API server enforces. it never takes a lease away by itself.");
    }

    /**
     * Two writers read the lease at the same version, and both try to put their own name in it.
     * The API server accepts the first and refuses the second, because the version it was based
     * on is no longer the current one. Returns what happened to the second.
     */
    static String twoWritesFromOneVersion(KubernetesClient client) {
        Lease first = client.leases().inNamespace(LeaseView.NAMESPACE).withName(LEASE).get();
        Lease second = client.leases().inNamespace(LeaseView.NAMESPACE).withName(LEASE).get();
        first.getSpec().setHolderIdentity("B");
        client.resource(first).update();
        second.getSpec().setHolderIdentity("C");
        try {
            client.resource(second).update();
            return "was accepted too";
        } catch (KubernetesClientException e) {
            return "refused with " + e.getCode() + " Conflict";
        }
    }

    private static void three(Cluster cluster) {
        System.out.println("THREE. The leader stops.");
        Inbox inbox = new Inbox(false);
        List<ServiceCopy> copies = electA(cluster, inbox, "B", "C");
        KubernetesClient client = cluster.client();
        try {
            long start = System.nanoTime();
            copies.get(0).stopCleanly();
            Poll.until("B or C to hold the lease", () -> Set.of("B", "C").contains(LeaseView.holder(client, LEASE)));
            Duration handover = Duration.ofNanos(System.nanoTime() - start);
            String next = LeaseView.holder(client, LEASE);
            String last = next.equals("B") ? "C" : "B";
            System.out.println("  A is shut down cleanly. on its way out, its elector hands the lease back by clearing the holder.");
            System.out.println("  one of B and C took over " + (handover.compareTo(Candidate.LEASE) < 0
                    ? "within a couple of seconds, well inside one " + LEASE_SECONDS + "-second lease"
                    : "only after a whole lease, which was not expected") + ".");

            ServiceCopy leader = copies.stream().filter(c -> c.name().equals(next)).findFirst().orElseThrow();
            start = System.nanoTime();
            leader.kill();
            Poll.until("the last copy to hold the lease", () -> LeaseView.holder(client, LEASE).equals(last));
            Duration gap = Duration.ofNanos(System.nanoTime() - start);
            System.out.println("  now the new leader is killed outright. it gets no chance to hand anything back.");
            System.out.println("  the lease went on naming the dead copy until it ran out. the last copy took over after "
                    + (gap.compareTo(Candidate.LEASE.minus(Candidate.RETRY.multipliedBy(2))) >= 0
                    ? "about one whole " + LEASE_SECONDS + "-second lease"
                    : "less than a lease, which was not expected") + ".");
            System.out.println("  for that time nobody was leading. the others cannot tell a dead leader from a slow one, so they wait.");
        } finally {
            copies.forEach(ServiceCopy::close);
        }
    }

    /** A checks it leads, then freezes. B takes the lease. What the lease says, before and after A wakes. */
    private record Frozen(List<ServiceCopy> copies, Inbox inbox, ZonedDateTime aLastRenewed, LeaseView whileFrozen, LeaseView whenASent) {
    }

    private static Frozen freezeTheLeader(Cluster cluster, boolean fencing) {
        KubernetesClient client = cluster.client();
        Inbox inbox = new Inbox(fencing);
        List<ServiceCopy> copies = electA(cluster, inbox, "B");
        ServiceCopy a = copies.get(0);
        ServiceCopy b = copies.get(1);
        a.tell("report-slowly");
        a.awaitSaying("CHECKED true");
        a.freeze();
        ZonedDateTime aLastRenewed = LeaseView.read(client, LEASE).orElseThrow().renewTime();
        b.awaitSaying("LEADING 1");
        LeaseView whileFrozen = LeaseView.read(client, LEASE).orElseThrow();
        b.tell("report");
        Poll.until("B's report to arrive", () -> inbox.received() == 1);
        a.wake();
        a.tell("go");
        Poll.until("A's report to arrive", () -> inbox.received() == 2);
        LeaseView whenASent = LeaseView.read(client, LEASE).orElseThrow();
        a.awaitSaying("STOPPED");
        return new Frozen(copies, inbox, aLastRenewed, whileFrozen, whenASent);
    }

    private static void four(Cluster cluster) {
        System.out.println("FOUR. Two who think they lead.");
        Frozen f = freezeTheLeader(cluster, false);
        try {
            System.out.println("  A checks that it leads, and starts building the report. then A freezes, as in a long garbage-collection pause.");
            System.out.println("  every thread in A stops, the one that renews the lease too. the lease runs out, and B takes it.");
            System.out.println("  the lease says: holder " + f.whileFrozen().holder() + ", holder changes " + f.whileFrozen().transitions() + ".");
            System.out.println("  B sends the report. A wakes up, still believing it leads, and sends too. the report was sent by: " + f.inbox().senders() + ".");
            System.out.println("  when A sent, the lease named " + f.whenASent().holder() + ", renewed after A's last renewal: "
                    + (f.whenASent().renewTime().isAfter(f.aLastRenewed()) ? "yes" : "no") + ".");
            System.out.println("  A's elector did tell it the lease was lost, but only once A woke up. A had checked before it froze.");
        } finally {
            f.copies().forEach(ServiceCopy::close);
        }
    }

    private static List<ServiceCopy> five(Cluster cluster) {
        System.out.println("FIVE. Fencing.");
        Frozen f = freezeTheLeader(cluster, true);
        ServiceCopy a = f.copies().get(0);
        ServiceCopy b = f.copies().get(1);
        String refusal = f.inbox().refusals().isEmpty() ? "accepted" : "refused, " + f.inbox().refusals().get(0).substring(3);
        System.out.println("  the same again, but each report now carries a token: the lease's count of holder changes when that copy took it.");
        System.out.println("  A's token is " + a.saidAfter("LEADING ") + ", B's is " + b.saidAfter("LEADING ") + ". B sends first. A wakes up and tries to send: " + refusal + ".");
        System.out.println("  the report was sent by: " + f.inbox().senders() + ". the count only goes up, and the inbox, the thing being written to, checks it.");
        return f.copies();
    }

    private static void six(Cluster cluster, ServiceCopy a, ServiceCopy b) {
        System.out.println("SIX. The bill.");
        KubernetesClient client = cluster.client();
        b.kill();
        Poll.until("the lease to be two whole leases old", () -> LeaseView.read(client, LEASE).orElseThrow().staleFor(2));
        String holder = LeaseView.holder(client, LEASE);
        System.out.println("  B is killed. A is still running, but its elector gave up when it lost the lease, and it never asks again.");
        System.out.println("  two whole leases later the lease still names " + holder + ", and nobody leads. the loser does not rejoin by itself.");
        a.tell("rejoin");
        a.awaitSaying("LEADING 2");
        System.out.println("  A starts a new elector, and leads again with token 2. the usual answer is simpler: a copy that loses the lease exits, and Kubernetes restarts it.");
        System.out.println("  a lease of " + LEASE_SECONDS + " seconds, renewed every " + RETRY_SECONDS + ": a dead leader goes unnoticed for up to " + LEASE_SECONDS
                + " seconds. make it shorter, and one slow moment costs a healthy leader its lease.");
        System.out.println("  the lease runs out by each copy's own clock, measured from a time the holder wrote. clocks that disagree break it.");
        System.out.println("  and all of it needs a Kubernetes API server: this demo ran 1 cluster, with 1 node, for 1 nightly report.");
    }
}
