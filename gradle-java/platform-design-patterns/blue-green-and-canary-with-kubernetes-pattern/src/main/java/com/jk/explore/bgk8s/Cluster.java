package com.jk.explore.bgk8s;

import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;

/** A real Kubernetes cluster, made with kind inside Docker, and the checkout manifests on it. */
public class Cluster {

    public static final String NAME = "patterns-bg";
    static final String CONTEXT = "kind-" + NAME;

    /** True when Docker is running and kind and kubectl are installed. */
    public static boolean toolsAvailable() {
        return Shell.works("docker", "info") && Shell.works("kind", "version") && Shell.works("kubectl", "version", "--client");
    }

    private static String resource(String name) {
        try (InputStream in = Cluster.class.getResourceAsStream("/k8s/" + name)) {
            return new String(in.readAllBytes(), StandardCharsets.UTF_8);
        } catch (IOException e) {
            throw new IllegalStateException(e);
        }
    }

    private static String kubectl(String... args) {
        String[] all = new String[args.length + 3];
        all[0] = "kubectl";
        all[1] = "--context";
        all[2] = CONTEXT;
        System.arraycopy(args, 0, all, 3, args.length);
        return Shell.run(all);
    }

    public void create() throws IOException {
        if (!Shell.run("kind", "get", "clusters").contains(NAME)) {
            Path config = Files.createTempFile("kind-config", ".yaml");
            Files.writeString(config, resource("kind-config.yaml"));
            Shell.run("kind", "create", "cluster", "--name", NAME, "--config", config.toString(), "--wait", "120s");
        }
        Shell.run("kind", "load", "docker-image", "nginx:alpine", "--name", NAME);
        Shell.runWithInput(resource("checkout.yaml"), "kubectl", "--context", CONTEXT, "apply", "-f", "-");
        selectVersion("v1");
        scale("checkout-v1", 2);
        scale("checkout-v2", 2);
    }

    public void delete() {
        Shell.run("kind", "delete", "cluster", "--name", NAME);
    }

    public void scale(String deployment, int replicas) {
        kubectl("scale", "deployment", deployment, "--replicas=" + replicas);
        if (replicas > 0) {
            kubectl("rollout", "status", "deployment/" + deployment, "--timeout=120s");
        } else {
            kubectl("wait", "--for=delete", "pod", "-l", "app=checkout,version=" + deployment.substring("checkout-".length()), "--timeout=120s");
        }
    }

    /** Blue-green: point the service at one release, and only that one. */
    public void selectVersion(String version) {
        kubectl("patch", "service", "checkout", "--type=merge", "-p",
                "{\"spec\":{\"selector\":{\"app\":\"checkout\",\"version\":\"" + version + "\"}}}");
    }

    /** Canary: point the service at every copy of the app, so traffic follows the replica counts. */
    public void selectBoth() {
        kubectl("patch", "service", "checkout", "--type=merge", "-p",
                "{\"spec\":{\"selector\":{\"app\":\"checkout\",\"version\":null}}}");
    }

    /** Pods that are ready, summed over both releases. */
    public int runningPods() {
        String out = kubectl("get", "deployments", "-l", "!none", "-o", "jsonpath={range .items[*]}{.status.readyReplicas}{\" \"}{end}");
        int total = 0;
        for (String n : out.strip().split("\\s+")) {
            if (!n.isBlank()) {
                total += Integer.parseInt(n);
            }
        }
        return total;
    }
}
