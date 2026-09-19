package com.jk.explore.sidecarkubernetes;

/**
 * <strong>Injection: the sidecar arrives beside a service whose own manifest
 * does not mention it.</strong> This is what a service mesh's admission step
 * does to every Pod as it is created. It returns a new spec; the original is
 * untouched, which is the point: the team that owns the service never edits it.
 */
public final class Injector {

    public static final ContainerSpec PROXY = new ContainerSpec("sidecar-proxy", "nginx:1.31.5-alpine", 8081);

    private Injector() {
    }

    public static PodSpec inject(PodSpec original) {
        boolean already = original.containers().stream().anyMatch(c -> c.name().equals(PROXY.name()));
        return already ? original : original.withContainer(PROXY);
    }
}
