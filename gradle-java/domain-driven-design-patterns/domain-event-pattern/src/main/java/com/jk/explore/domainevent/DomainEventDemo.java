package com.jk.explore.domainevent;

import com.jk.explore.domainevent.domain.DomainEvent;
import com.jk.explore.domainevent.domain.Order;
import com.jk.explore.domainevent.infrastructure.Handlers;
import com.jk.explore.domainevent.infrastructure.Journal;
import com.jk.explore.domainevent.infrastructure.OrderRepository;
import com.jk.explore.domainevent.naive.NaivePlaceOrder;

import java.util.List;

public class DomainEventDemo {

    /** The shop: a repository whose relay delivers to stock, email and analytics. */
    static final class Shop {
        final Journal journal = new Journal();
        final Handlers.ConfirmationEmail email = new Handlers.ConfirmationEmail(journal);
        final OrderRepository orders = new OrderRepository(List.of(new Handlers.StockReservation(journal), email, new Handlers.FunnelCounter(journal)));
    }

    public static void main(String[] args) {
        one();
        two();
        three();
        four();
        five();
        six();
    }

    private static void one() {
        System.out.println("ONE. The order calls everyone.");
        Journal journal = new Journal();
        NaivePlaceOrder naive = new NaivePlaceOrder(journal);
        naive.mailServerDown(true);
        try {
            naive.place("ORD-1", "ada", 4999);
        } catch (IllegalStateException e) {
            System.out.println("  the mail server is down. the caller gets: " + e.getMessage() + ".");
        }
        System.out.println("  order saved: " + naive.isSaved("ORD-1") + ". what happened: " + journal.lines() + ".");
        System.out.println("  saved and reserved, the customer told they failed, analytics never counted it.");
    }

    private static void two() {
        System.out.println("TWO. The order says what happened.");
        Order order = new Order("ORD-2", "ada", 4999);
        order.place();
        List<DomainEvent> events = order.pullEvents();
        System.out.println("  events recorded by place(): " + events + ".");
        System.out.println("  the order called nobody. asked again: " + order.pullEvents() + ".");
    }

    private static void three() {
        System.out.println("THREE. Delivered after the save.");
        Shop shop = new Shop();
        Order order = new Order("ORD-3", "ada", 4999);
        order.place();
        shop.orders.save(order);
        System.out.println("  saved. events waiting: " + shop.orders.pending() + ". reactions so far: " + shop.journal.lines().size() + ".");
        shop.orders.relay();
        shop.journal.lines().forEach(l -> System.out.println("  " + l));
        System.out.println("  events waiting now: " + shop.orders.pending() + ".");
    }

    private static void four() {
        System.out.println("FOUR. A failing reaction does not undo the order.");
        Shop shop = new Shop();
        shop.email.mailServerDown(true);
        Order order = new Order("ORD-4", "ada", 4999);
        order.place();
        shop.orders.save(order);
        List<String> failures = shop.orders.relay();
        System.out.println("  the mail server is down. failures: " + failures + ".");
        System.out.println("  the others still ran: " + shop.journal.lines() + ".");
        System.out.println("  events still waiting: " + shop.orders.pending() + ".");
        shop.email.mailServerDown(false);
        System.out.println("  the mail server is back. a second relay: " + shop.orders.relay() + " failures, waiting: " + shop.orders.pending() + ".");
        System.out.println("  the email went out once: " + shop.journal.lines().stream().filter(l -> l.startsWith("email")).count() + ", and stock was not reserved twice: "
                + shop.journal.lines().stream().filter(l -> l.startsWith("stock")).count() + ".");
    }

    private static void five() {
        System.out.println("FIVE. Events are facts.");
        Order order = new Order("ORD-5", "ada", 4999);
        order.place();
        order.cancel("changed my mind");
        List<DomainEvent> events = order.pullEvents();
        System.out.println("  place then cancel: " + events.stream().map(e -> e.getClass().getSimpleName()).toList() + ", in that order.");
        System.out.println("  each event is a record: it carries the order id and the data, not the order.");
        System.out.println("  a handler that receives one cannot reach back and change the order.");
    }

    private static void six() {
        System.out.println("SIX. The bill: the gap between saving and telling.");
        Shop shop = new Shop();
        Order order = new Order("ORD-6", "ada", 4999);
        order.place();
        shop.orders.save(order);
        System.out.println("  the process stops after the save and before the relay. reactions: " + shop.journal.lines().size() + ". events kept: " + shop.orders.pending() + ".");
        shop.orders.relay();
        System.out.println("  after a restart the relay runs. reactions: " + shop.journal.lines().size() + ". nothing was lost, because the events were saved with the order.");
        System.out.println("  publishing straight after the save, with no outbox, would have lost all three.");
    }
}
