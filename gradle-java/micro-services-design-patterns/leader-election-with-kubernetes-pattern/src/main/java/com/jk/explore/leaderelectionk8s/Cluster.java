package com.jk.explore.leaderelectionk8s;

import io.fabric8.kubernetes.client.Config;
import io.fabric8.kubernetes.client.KubernetesClient;
import io.fabric8.kubernetes.client.KubernetesClientBuilder;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

/**
 * A real Kubernetes cluster with one node, made by kind inside the container runtime, and
 * deleted again when this object is closed.
 *
 * <p>kind normally writes the new cluster's address into your own ~/.kube/config. This class
 * gives it a private file instead, so the demo leaves your Kubernetes settings exactly as it
 * found them.
 */
public final class Cluster implements AutoCloseable {

    /** Unique to this project, so it never touches a cluster anything else made. */
    public static final String NAME = "patterns-leader-election";

    /** The node image kind v0.33.0 uses by default, pinned so every run gets Kubernetes 1.37.0. */
    public static final String NODE_IMAGE =
            "kindest/node:v1.37.0@sha256:a1ed56cfb0e7b93589bdf97c8cd566405a265939e3620fc4f5de89adff580ae5";

    /** What to say when there is no container runtime to run the cluster in. */
    public static final String NO_RUNTIME_ADVICE =
            "This demo needs a container runtime, because it starts a real Kubernetes cluster inside one.\n"
            + "Start Docker Desktop, or any Docker-compatible runtime, wait until it says it is running, and run ./gradlew run again.";

    /** What to say when the runtime is there but kind is not. */
    public static final String NO_KIND_ADVICE =
            "This demo needs kind, the tool that runs a Kubernetes cluster inside a container.\n"
            + "Install it (on a Mac: brew install kind; elsewhere see kind.sigs.k8s.io), and run ./gradlew run again.";

    /** What to say when both are there but the cluster will not come up. */
    public static final String WOULD_NOT_START_ADVICE =
            "The Kubernetes cluster would not start. kind needs about 1 GB of memory free in the container runtime,\n"
            + "and the first run downloads the node image. Check both, then run ./gradlew run again.";

    private final Path kubeconfig;
    private KubernetesClient client;

    public Cluster() {
        try {
            this.kubeconfig = Files.createTempFile(NAME + "-", ".kubeconfig");
        } catch (IOException e) {
            throw new IllegalStateException(e);
        }
    }

    public static boolean containerRuntimeAvailable() {
        return Shell.works("docker", "info");
    }

    public static boolean kindAvailable() {
        return Shell.works("kind", "version");
    }

    /** Creates the cluster, first removing one of the same name that an interrupted run left behind. */
    public void create() {
        if (Shell.run("kind", "get", "clusters").lines().anyMatch(NAME::equals)) {
            Shell.run("kind", "delete", "cluster", "--name", NAME);
        }
        Shell.run("kind", "create", "cluster", "--name", NAME, "--image", NODE_IMAGE,
                "--kubeconfig", kubeconfig.toString(), "--wait", "120s");
        client = connect(kubeconfig);
    }

    /** The private kubeconfig file. Each copy of the service is handed this path. */
    public Path kubeconfig() {
        return kubeconfig;
    }

    /** The demo's own connection to the API server, used to read the lease and never to lead. */
    public KubernetesClient client() {
        return client;
    }

    public static KubernetesClient connect(Path kubeconfig) {
        try {
            return new KubernetesClientBuilder().withConfig(Config.fromKubeconfig(Files.readString(kubeconfig))).build();
        } catch (IOException e) {
            throw new IllegalStateException(e);
        }
    }

    @Override
    public void close() {
        if (client != null) {
            client.close();
        }
        Shell.works("kind", "delete", "cluster", "--name", NAME, "--kubeconfig", kubeconfig.toString());
        try {
            Files.deleteIfExists(kubeconfig);
        } catch (IOException ignored) {
            // a temporary file; the system clears it eventually
        }
    }
}
