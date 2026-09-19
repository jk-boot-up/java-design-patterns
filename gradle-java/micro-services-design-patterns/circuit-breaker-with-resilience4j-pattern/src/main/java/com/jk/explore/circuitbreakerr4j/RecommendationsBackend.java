package com.jk.explore.circuitbreakerr4j;

import org.springframework.stereotype.Component;

import java.util.List;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;

/** The remote service, in memory: it counts every call that reaches it, and can be switched off. */
@Component
public class RecommendationsBackend {

    private final AtomicBoolean down = new AtomicBoolean();
    private final AtomicInteger calls = new AtomicInteger();

    public void down(boolean down) {
        this.down.set(down);
    }

    public int calls() {
        return calls.get();
    }

    public List<String> recommendationsFor(String sku) {
        calls.incrementAndGet();
        if (down.get()) {
            throw new BackendDown();
        }
        if (sku == null || sku.isBlank()) {
            throw new IllegalArgumentException("no such product");
        }
        return List.of("Blue Mug Set", "Tea Towel");
    }
}
