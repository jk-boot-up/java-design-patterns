package com.jk.explore.domainevent.infrastructure;

import com.jk.explore.domainevent.domain.DomainEvent;
import com.jk.explore.domainevent.domain.OrderCancelled;
import com.jk.explore.domainevent.domain.OrderPlaced;

import java.util.concurrent.atomic.AtomicBoolean;

/** The three reactions to an order being placed. */
public final class Handlers {

    private Handlers() {
    }

    public static final class StockReservation implements EventHandler {
        private final Journal journal;

        public StockReservation(Journal journal) {
            this.journal = journal;
        }

        public String name() {
            return "stock";
        }

        public void handle(DomainEvent event) {
            if (event instanceof OrderPlaced placed) {
                journal.add("stock: reserved for " + placed.orderId());
            } else if (event instanceof OrderCancelled cancelled) {
                journal.add("stock: released for " + cancelled.orderId());
            }
        }
    }

    public static final class ConfirmationEmail implements EventHandler {
        private final Journal journal;
        private final AtomicBoolean mailServerDown = new AtomicBoolean();

        public ConfirmationEmail(Journal journal) {
            this.journal = journal;
        }

        public void mailServerDown(boolean down) {
            mailServerDown.set(down);
        }

        public String name() {
            return "email";
        }

        public void handle(DomainEvent event) {
            if (mailServerDown.get()) {
                throw new IllegalStateException("mail server timed out");
            }
            if (event instanceof OrderPlaced placed) {
                journal.add("email: confirmed " + placed.orderId() + " to " + placed.customerId());
            }
        }
    }

    public static final class FunnelCounter implements EventHandler {
        private final Journal journal;

        public FunnelCounter(Journal journal) {
            this.journal = journal;
        }

        public String name() {
            return "analytics";
        }

        public void handle(DomainEvent event) {
            if (event instanceof OrderPlaced placed) {
                journal.add("analytics: counted " + placed.orderId() + " for " + placed.totalPence() + " pence");
            }
        }
    }
}
