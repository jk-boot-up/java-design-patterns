package com.jk.explore.lazyloadhibernate;

import com.jk.explore.lazyloadhibernate.domain.CustomerOrder;
import org.hibernate.Session;
import org.hibernate.SessionFactory;

import java.util.ArrayList;
import java.util.List;

/**
 * A page listing every order with its customer's name, loaded four ways. The
 * first three are the usual answers to a lazy load that fails, or is slow.
 */
public class OrderPage {

    /** A row of the page, and nothing else. */
    public record OrderRow(int orderId, String customerName) {
    }

    private final SessionFactory factory;

    public OrderPage(SessionFactory factory) {
        this.factory = factory;
    }

    /** Lazy, session closed before the page is rendered. Fails. */
    public List<CustomerOrder> loadOrdersAndClose() {
        try (Session session = factory.openSession()) {
            return session.createQuery("from CustomerOrder", CustomerOrder.class).getResultList();
        }
    }

    /** Fix one: keep the session open while the page renders. Works, and issues one query per order inside the view. */
    public List<String> renderWithSessionOpen() {
        try (Session session = factory.openSession()) {
            List<String> page = new ArrayList<>();
            for (CustomerOrder order : session.createQuery("from CustomerOrder", CustomerOrder.class).getResultList()) {
                page.add("order " + order.id() + " for " + order.customer().name());
            }
            return page;
        }
    }

    /** Fix two: fetch the customer in the same query. */
    public List<String> renderWithJoinFetch() {
        try (Session session = factory.openSession()) {
            List<String> page = new ArrayList<>();
            for (CustomerOrder order : session.createQuery(
                    "select o from CustomerOrder o join fetch o.customer", CustomerOrder.class).getResultList()) {
                page.add("order " + order.id() + " for " + order.customer().name());
            }
            return page;
        }
    }

    /** A page showing how many lines each order has. The lines are lazy, so each order costs its own statement. */
    public List<String> renderLineCountsWithSessionOpen() {
        try (Session session = factory.openSession()) {
            List<String> page = new ArrayList<>();
            for (CustomerOrder order : session.createQuery("from CustomerOrder", CustomerOrder.class).getResultList()) {
                page.add("order " + order.id() + " has " + order.lines().size() + " lines");
            }
            return page;
        }
    }

    /** The same page, fetching every order's lines in the one query. */
    public List<String> renderLineCountsWithJoinFetch() {
        try (Session session = factory.openSession()) {
            List<String> page = new ArrayList<>();
            for (CustomerOrder order : session.createQuery(
                    "select o from CustomerOrder o join fetch o.lines", CustomerOrder.class).getResultList()) {
                page.add("order " + order.id() + " has " + order.lines().size() + " lines");
            }
            return page;
        }
    }

    /** How many rows the database sends for that join. Hibernate then folds the repeats into 20 orders. */
    public long rowsTheJoinProduces() {
        try (Session session = factory.openSession()) {
            return session.createQuery("select count(*) from CustomerOrder o join o.lines l", Long.class).getSingleResult();
        }
    }

    /** Fix three: ask for exactly the columns the page needs, as a DTO. */
    public List<OrderRow> renderWithProjection() {
        try (Session session = factory.openSession()) {
            return session.createQuery(
                    "select new com.jk.explore.lazyloadhibernate.OrderPage$OrderRow(o.id, c.name) from CustomerOrder o join o.customer c",
                    OrderRow.class).getResultList();
        }
    }
}
