package com.jk.explore.servicemesh;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeMap;

/**
 * Every service has a proxy beside it. The proxies do the retrying, the identity check and the counting,
 * to one policy that is set in one place. The services themselves know nothing of it.
 */
public class Mesh {

    /** Ticks for one attempt when it goes through two proxies: one out, one in, and the network hop. */
    public static final int TICKS_THROUGH_PROXIES = 3;
    /** Ticks for one attempt made directly. */
    public static final int TICKS_DIRECT = 1;

    private final Map<String, Backend> services = new HashMap<>();
    private final Map<String, Set<String>> allowed = new HashMap<>();
    private final Map<String, int[]> metrics = new TreeMap<>();
    private int retries;
    private int ticks;
    private int denied;
    private int proxyCount;

    public void register(String name, Backend backend) {
        services.put(name, backend);
        proxyCount++;
    }

    public void setRetries(int retries) {
        this.retries = retries;
    }

    public void allowOnly(String callee, Set<String> callers) {
        allowed.put(callee, callers);
    }

    /** The caller's proxy presents the caller's identity, so a service cannot claim to be another. */
    public boolean call(String caller, String callee) {
        Set<String> ok = allowed.get(callee);
        if (ok != null && !ok.contains(caller)) {
            denied++;
            return false;
        }
        int[] m = metrics.computeIfAbsent(caller + "->" + callee, k -> new int[3]);
        m[0]++;
        for (int attempt = 0; attempt <= retries; attempt++) {
            ticks += TICKS_THROUGH_PROXIES;
            m[2]++;
            if (services.get(callee).call()) {
                return true;
            }
        }
        m[1]++;
        return false;
    }

    /** A line per pair: calls, failed calls, and attempts made. */
    public List<String> report() {
        return metrics.entrySet().stream()
                .map(e -> e.getKey() + " calls " + e.getValue()[0] + ", failed " + e.getValue()[1] + ", attempts " + e.getValue()[2])
                .toList();
    }

    public int ticks() {
        return ticks;
    }

    public int denied() {
        return denied;
    }

    public int proxies() {
        return proxyCount;
    }
}
