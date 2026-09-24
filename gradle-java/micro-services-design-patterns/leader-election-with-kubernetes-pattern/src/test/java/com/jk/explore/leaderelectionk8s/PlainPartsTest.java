package com.jk.explore.leaderelectionk8s;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.time.ZoneOffset;
import java.time.ZonedDateTime;
import java.util.List;
import org.junit.jupiter.api.Test;

/** The parts that need no cluster: the inbox, the lease arithmetic and the timings. */
class PlainPartsTest {

    @Test
    void anInboxThatDoesNotCheckTakesEveryReport() {
        Inbox inbox = new Inbox(false);
        inbox.receive("B", 1);
        inbox.receive("A", 0);
        assertEquals(List.of("B", "A"), inbox.senders());
        assertEquals(2, inbox.received());
    }

    @Test
    void aFencingInboxRefusesAnOlderToken() {
        Inbox inbox = new Inbox(true);
        inbox.receive("B", 1);
        inbox.receive("A", 0);
        assertEquals(List.of("B"), inbox.senders());
        assertEquals(List.of("A: token 0 is older than 1"), inbox.refusals());
    }

    @Test
    void aFencingInboxAcceptsTheSameTokenAgainAndANewerOne() {
        Inbox inbox = new Inbox(true);
        inbox.receive("A", 0);
        inbox.receive("A", 0);
        inbox.receive("B", 1);
        assertEquals(List.of("A", "A", "B"), inbox.senders());
        assertTrue(inbox.refusals().isEmpty());
    }

    @Test
    void aLeaseIsStaleOnlyOnceItsWholeLengthHasPassed() {
        ZonedDateTime now = ZonedDateTime.now(ZoneOffset.UTC);
        assertFalse(new LeaseView("A", 0, now, 5, "1").staleFor(1));
        assertTrue(new LeaseView("A", 0, now.minusSeconds(11), 5, "1").staleFor(2));
        assertFalse(new LeaseView("A", 0, now.minusSeconds(9), 5, "1").staleFor(2));
    }

    @Test
    void theTimingsAreOnesFabric8Accepts() {
        // Fabric8 refuses a configuration unless lease > renew deadline > retry * 2.2.
        assertTrue(Candidate.LEASE.compareTo(Candidate.RENEW_DEADLINE) > 0);
        assertTrue(Candidate.RENEW_DEADLINE.toMillis() > Candidate.RETRY.toMillis() * 2.2);
    }
}
