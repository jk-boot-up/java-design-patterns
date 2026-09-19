package com.jk.explore.sidecarkubernetes;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * <strong>Docker Compose, for comparison.</strong> Two containers share a
 * network only if the file says so: {@code network_mode: "service:checkout"}.
 * Each container is otherwise on its own, with its own lifecycle.
 */
public final class Compose {

    private final Map<String, NetworkNamespace> namespaces = new HashMap<>();
    private final Map<String, Container> containers = new HashMap<>();
    private final List<String> events = new ArrayList<>();
    private int nextAddress = 2;

    /** Starts a container in its own network, unless it names a service whose network to join. */
    public Container up(ContainerSpec spec, String networkModeService) {
        NetworkNamespace ns = networkModeService == null
                ? new NetworkNamespace("172.18.0." + nextAddress++)
                : namespaces.get(networkModeService);
        Container container = new Container(spec);
        namespaces.put(spec.name(), ns);
        containers.put(spec.name(), container);
        if (spec.port() != 0) {
            ns.listen(spec.port(), container);
        }
        return container;
    }

    /** Can container {@code from} reach the given port on localhost? Only if it shares a network with a listener. */
    public boolean localhostReaches(String from, int port) {
        return namespaces.get(from).reachable(port);
    }

    public void stop(String name) {
        containers.get(name).crash();
        events.add(name + " stopped; nothing else did");
    }

    public boolean running(String name) {
        return containers.get(name).running();
    }
}
