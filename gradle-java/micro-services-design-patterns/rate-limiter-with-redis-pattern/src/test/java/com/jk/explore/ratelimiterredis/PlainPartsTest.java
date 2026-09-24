package com.jk.explore.ratelimiterredis;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import io.github.bucket4j.Bucket;
import java.time.Duration;
import java.util.List;
import org.junit.jupiter.api.Test;

/** The parts that need no Redis at all. */
class PlainPartsTest {

    @Test
    void anInMemoryBucketAllowsTenThenRefuses() {
        Bucket bucket = SearchLimit.inMemoryBucket();
        int allowed = 0;
        for (int i = 0; i < 20; i++) {
            if (bucket.tryConsume(1)) {
                allowed++;
            }
        }
        assertEquals(10, allowed);
        assertFalse(bucket.tryConsume(1));
    }

    @Test
    void threeServersWithTheirOwnBucketsLetThreeTimesTheLimitThrough() {
        List<ServerWithOwnBuckets> servers = List.of(new ServerWithOwnBuckets(), new ServerWithOwnBuckets(), new ServerWithOwnBuckets());
        int allowed = 0;
        for (int i = 0; i < 90; i++) {
            if (servers.get(i % 3).search("client-42")) {
                allowed++;
            }
        }
        assertEquals(30, allowed);
        servers.forEach(server -> assertEquals(1, server.bucketsHeld()));
    }

    @Test
    void eachClientHasABucketOfItsOwnOnOneServer() {
        ServerWithOwnBuckets server = new ServerWithOwnBuckets();
        for (int i = 0; i < 10; i++) {
            assertTrue(server.search("client-42"));
        }
        assertFalse(server.search("client-42"));
        assertTrue(server.search("client-77"), "another client is not held back by the first");
        assertEquals(2, server.bucketsHeld());
    }

    @Test
    void theRuleIsTenAnHourAndEachClientHasItsOwnKey() {
        assertEquals(10, SearchLimit.configuration().getBandwidths()[0].getCapacity());
        assertEquals(Duration.ofHours(1), SearchLimit.REFILL_EVERY);
        assertEquals("search-limit:client-42", SearchLimit.keyFor("client-42"));
    }

    @Test
    void aWaitThatNeverComesTrueFailsAndSaysWhatItWasWaitingFor() {
        IllegalStateException failure = assertThrows(IllegalStateException.class,
                () -> Poll.until("the sky to fall in", Duration.ofMillis(200), () -> false));
        assertTrue(failure.getMessage().contains("the sky to fall in"), failure.getMessage());
    }

    @Test
    void aWaitReturnsAsSoonAsTheConditionIsTrue() {
        int[] asked = {0};
        Poll.until("the third question", Duration.ofSeconds(5), () -> ++asked[0] == 3);
        assertEquals(3, asked[0]);
    }

    @Test
    void withNoContainerRuntimeTheDemoSaysWhatToDoAboutIt() {
        assertTrue(Redis.NO_RUNTIME_ADVICE.contains("container runtime"), Redis.NO_RUNTIME_ADVICE);
        assertTrue(Redis.NO_RUNTIME_ADVICE.contains("./gradlew run again"), Redis.NO_RUNTIME_ADVICE);
    }
}
