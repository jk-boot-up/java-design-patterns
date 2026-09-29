package com.jk.explore.secrets;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.util.Set;
import org.junit.jupiter.api.Test;

class SecretsManagerTest {

    private final SecretsManager manager = new SecretsManager();

    @Test
    void latestVersionIsHandedOut() {
        manager.store("k", "a", Set.of("svc"));
        manager.rotate("k", "b");
        assertEquals("b", manager.read("svc", "k"));
    }

    @Test
    void unknownSecretIsDenied() {
        assertThrows(SecurityException.class, () -> manager.read("svc", "nope"));
    }

    @Test
    void cacheHoldsUntilTtl() {
        manager.store("k", "a", Set.of("svc"));
        CachedSecret cached = new CachedSecret(manager, "svc", "k", 100);
        assertEquals("a", cached.get(0));
        manager.rotate("k", "b");
        assertEquals("a", cached.get(99));
        assertEquals("b", cached.get(100));
    }
}
