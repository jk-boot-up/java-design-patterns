package com.jk.explore.sidecarkubernetes;

import java.util.ArrayList;
import java.util.List;

/**
 * <strong>A Pod's manifest.</strong> The service container, and any sidecars
 * beside it. {@code sidecarsFirst} models Kubernetes' native sidecar containers:
 * a sidecar declared as an init container with {@code restartPolicy: Always}
 * is started, and must be running, before the main containers start.
 */
public record PodSpec(String name, List<ContainerSpec> containers, boolean sidecarsFirst) {

    public static PodSpec of(String name, ContainerSpec service) {
        return new PodSpec(name, List.of(service), false);
    }

    public PodSpec withContainer(ContainerSpec added) {
        List<ContainerSpec> all = new ArrayList<>(containers);
        all.add(added);
        return new PodSpec(name, List.copyOf(all), sidecarsFirst);
    }

    public PodSpec withSidecarsFirst(boolean first) {
        return new PodSpec(name, containers, first);
    }
}
