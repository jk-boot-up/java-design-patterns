package com.jk.explore.plugin;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all = String.join("\n", PluginDemo.run());

    @Test
    void scattered() {
        assertTrue(all.contains("staging: REAL email to priya@example.com"));
    }

    @Test
    void plugins() {
        assertTrue(all.contains("dev: fake gateway approved £63.44 for ORD-1"));
        assertTrue(all.contains("prod: REAL card charged £63.44 for ORD-1"));
        assertTrue(all.contains("staging: sandbox inbox kept email to priya@example.com"));
    }

    @Test
    void startupCheck() {
        assertTrue(all.contains("startup check: demo: cannot create com.jk.explore.plugin.Implementations$SandboxEmaler for Emailer"));
    }
}
