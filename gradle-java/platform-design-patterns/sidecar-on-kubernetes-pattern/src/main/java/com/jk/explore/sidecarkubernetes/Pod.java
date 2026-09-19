package com.jk.explore.sidecarkubernetes;

import java.util.ArrayList;
import java.util.List;

/**
 * <strong>A Pod: containers that share a network namespace and a fate.</strong>
 * The sharing is not configured. It is what a Pod is. There is no way to put two
 * containers in one Pod and give them separate networks, and no way to schedule,
 * evict or delete one of them without the other.
 */
public final class Pod {

    private final PodSpec spec;
    private final NetworkNamespace network;
    private final List<Container> containers = new ArrayList<>();
    private final List<String> startOrder = new ArrayList<>();
    private boolean deleted;

    Pod(PodSpec spec, String address) {
        this.spec = spec;
        this.network = new NetworkNamespace(address);
    }

    void start(ContainerSpec container) {
        Container started = new Container(container);
        containers.add(started);
        startOrder.add(container.name());
        if (container.port() != 0) {
            network.listen(container.port(), started);
        }
    }

    public PodSpec spec() {
        return spec;
    }

    public NetworkNamespace network() {
        return network;
    }

    public List<Container> containers() {
        return List.copyOf(containers);
    }

    public Container container(String name) {
        return containers.stream().filter(c -> c.name().equals(name)).findFirst().orElseThrow();
    }

    public List<String> startOrder() {
        return List.copyOf(startOrder);
    }

    public boolean deleted() {
        return deleted;
    }

    void delete() {
        deleted = true;
        containers.forEach(Container::crash);
    }

    public int readyCount() {
        return (int) containers.stream().filter(Container::running).count();
    }

    /** What {@code kubectl get pods} prints in the READY column. */
    public String ready() {
        return readyCount() + "/" + containers.size();
    }

    /** A Pod is ready for traffic only when every container in it is. */
    public boolean isReady() {
        return !deleted && readyCount() == containers.size();
    }
}
