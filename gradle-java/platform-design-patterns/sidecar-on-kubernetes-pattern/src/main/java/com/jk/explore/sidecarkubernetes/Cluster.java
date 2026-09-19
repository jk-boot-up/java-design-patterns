package com.jk.explore.sidecarkubernetes;

/**
 * <strong>A control plane, in about twenty lines.</strong> It schedules a Pod
 * from a manifest, gives it a new address, deletes it as one unit, and runs the
 * kubelet's loop that restarts a crashed container. It is a model: it has no
 * scheduler, no etcd and no network partitions, and says so.
 */
public final class Cluster {

    private int nextAddress = 10;

    public Pod schedule(PodSpec spec) {
        Pod pod = new Pod(spec, "10.244.0." + nextAddress++);
        if (spec.sidecarsFirst()) {
            spec.containers().stream().skip(1).forEach(pod::start);
            pod.start(spec.containers().get(0));
        } else {
            spec.containers().forEach(pod::start);
        }
        return pod;
    }

    /** Deleting a Pod deletes every container in it. There is no other unit to delete. */
    public void delete(Pod pod) {
        pod.delete();
    }

    /** A container's process dies. The Pod, and its other containers, carry on. */
    public void crash(Pod pod, String containerName) {
        pod.container(containerName).crash();
    }

    /** The kubelet's loop. With {@code restartPolicy: Always} it restarts each crashed container, one at a time. */
    public void kubeletReconciles(Pod pod) {
        if (pod.deleted()) {
            return;
        }
        pod.containers().stream().filter(c -> !c.running()).forEach(Container::restart);
    }
}
