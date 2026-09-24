package com.jk.explore.leaderelectionk8s;

import io.fabric8.kubernetes.api.model.coordination.v1.Lease;
import io.fabric8.kubernetes.client.KubernetesClient;
import java.time.ZoneOffset;
import java.time.ZonedDateTime;
import java.util.Optional;

/**
 * What the Lease object in the API server says right now: who holds it, how many times the
 * holder has changed, and when the holder last renewed it.
 *
 * <p>The demo reads the lease with its own connection, as an outside observer. It never writes
 * to it, except in the one place that shows the API server refusing a stale write.
 */
public record LeaseView(String holder, int transitions, ZonedDateTime renewTime, int durationSeconds, String version) {

    public static final String NAMESPACE = "default";

    public static Optional<LeaseView> read(KubernetesClient client, String name) {
        Lease lease = client.leases().inNamespace(NAMESPACE).withName(name).get();
        if (lease == null || lease.getSpec() == null) {
            return Optional.empty();
        }
        var spec = lease.getSpec();
        return Optional.of(new LeaseView(
                spec.getHolderIdentity() == null ? "" : spec.getHolderIdentity(),
                spec.getLeaseTransitions() == null ? 0 : spec.getLeaseTransitions(),
                spec.getRenewTime(),
                spec.getLeaseDurationSeconds() == null ? 0 : spec.getLeaseDurationSeconds(),
                lease.getMetadata().getResourceVersion()));
    }

    /** The holder named in the lease, or an empty string when there is no lease or no holder. */
    public static String holder(KubernetesClient client, String name) {
        return read(client, name).map(LeaseView::holder).orElse("");
    }

    /** Removes the lease, so the next act starts from nothing, and waits until it is gone. */
    public static void delete(KubernetesClient client, String name) {
        client.leases().inNamespace(NAMESPACE).withName(name).delete();
        Poll.until("the lease " + name + " to be deleted", () -> read(client, name).isEmpty());
    }

    /** True once the lease's last renewal is more than {@code leases} whole lease lengths ago. */
    public boolean staleFor(int leases) {
        return ZonedDateTime.now(ZoneOffset.UTC).isAfter(renewTime.plusSeconds((long) durationSeconds * leases));
    }
}
