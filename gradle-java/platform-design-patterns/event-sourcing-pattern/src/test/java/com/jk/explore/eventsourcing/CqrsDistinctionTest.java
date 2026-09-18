package com.jk.explore.eventsourcing;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.time.LocalDate;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;

/**
 * Event sourcing and CQRS are two patterns, not one, and this test holds them apart
 * by building each of them without the other.
 *
 * <p>The short version, worth memorising: CQRS changes where reads come from. Event
 * sourcing changes what the writes store.
 */
class CqrsDistinctionTest {

    private static final LocalDate MAR_1 = LocalDate.of(2025, 3, 1);
    private static final LocalDate MAR_8 = LocalDate.of(2025, 3, 8);

    @Test
    @DisplayName("CQRS with no event sourcing: a second read-shaped model, no log")
    void cqrsWithoutEventSourcing() {
        CurrentStateLoyaltyAccounts writeSide = new CurrentStateLoyaltyAccounts();
        OrderHistoryReadModel readSide = new OrderHistoryReadModel();

        // The write side updates a row. The read side is told separately, and
        // serves the history page. There is no event log in this test at all.
        writeSide.award("C-4417", 60, "ORD-8801", MAR_1);
        readSide.recordOrder("C-4417", "ORD-8801", 60);
        writeSide.award("C-4417", 120, "ORD-8907", MAR_8);
        readSide.recordOrder("C-4417", "ORD-8907", 120);

        assertEquals(180, writeSide.balanceFor("C-4417"));
        assertEquals(List.of("order ORD-8801 for £60", "order ORD-8907 for £120"),
                readSide.historyFor("C-4417"));
    }

    @Test
    @DisplayName("and the read model can drift, which is the cost CQRS brings on its own")
    void theReadModelCanFallBehind() {
        CurrentStateLoyaltyAccounts writeSide = new CurrentStateLoyaltyAccounts();
        OrderHistoryReadModel readSide = new OrderHistoryReadModel();

        writeSide.award("C-4417", 60, "ORD-8801", MAR_1);
        // The update to the read side is lost — a dropped message, a failed job.
        // Nothing throws. The customer sees an empty history and a balance of 60.
        assertEquals(60, writeSide.balanceFor("C-4417"));
        assertEquals(List.of(), readSide.historyFor("C-4417"));
    }

    @Test
    @DisplayName("event sourcing with no CQRS: reads fold the very same events writes appended")
    void eventSourcingWithoutCqrs() {
        LoyaltyEventStore store = new LoyaltyEventStore();
        EventSourcedLoyaltyAccounts accounts = new EventSourcedLoyaltyAccounts(store);

        accounts.award("C-4417", 60, "ORD-8801", MAR_1);
        accounts.award("C-4417", 120, "ORD-8907", MAR_8);

        // One model. The read walks the same list the write appended to, so there
        // is nothing to fall behind and nothing to drift.
        assertEquals(180, accounts.balanceFor("C-4417"));
        assertEquals(2, accounts.explain("C-4417").size());
        assertEquals(2, store.size());
    }

    @Test
    @DisplayName("neither pattern implies the other, so the trade-offs are separate")
    void theTwoPatternsAreIndependent() {
        // The CQRS example above has two models and no log. The event sourcing
        // example has a log and one model. A design can have either, both, or
        // neither, and the costs to weigh are different in each case: staleness
        // for CQRS, replay cost and schema versioning for event sourcing.
        OrderHistoryReadModel readSide = new OrderHistoryReadModel();
        readSide.recordOrder("C-4417", "ORD-8801", 60);
        assertFalse(readSide.historyFor("C-4417").isEmpty());

        LoyaltyEventStore store = new LoyaltyEventStore();
        new EventSourcedLoyaltyAccounts(store).award("C-4417", 60, "ORD-8801", MAR_1);
        assertEquals(1, store.size());
    }
}
