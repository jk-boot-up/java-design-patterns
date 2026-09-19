package com.jk.explore.microkernel;

import java.util.ArrayList;
import java.util.List;

/** The small core: it keeps plugins, starts and stops them, and runs them in order. */
public class Kernel {

    private final List<Plugin> plugins = new ArrayList<>();
    private final List<String> failures = new ArrayList<>();

    public void register(Plugin plugin) {
        plugin.start();
        plugins.add(plugin);
    }

    public boolean unregister(String name) {
        for (Plugin p : plugins) {
            if (p.name().equals(name)) {
                p.stop();
                plugins.remove(p);
                return true;
            }
        }
        return false;
    }

    public long total(long baseCents) {
        long total = baseCents;
        for (Plugin p : List.copyOf(plugins)) {
            try {
                total = p.adjust(total);
            } catch (RuntimeException e) {
                failures.add(p.name() + ": " + e.getMessage());
            }
        }
        return total;
    }

    public List<String> names() {
        return plugins.stream().map(Plugin::name).toList();
    }

    public List<String> failures() {
        return List.copyOf(failures);
    }
}
