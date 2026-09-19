package com.jk.explore.lazyloadhibernate;

import com.jk.explore.lazyloadhibernate.domain.Customer;
import com.jk.explore.lazyloadhibernate.domain.CustomerOrder;
import org.hibernate.Hibernate;
import org.hibernate.LazyInitializationException;
import org.hibernate.Session;
import org.hibernate.SessionFactory;

import java.util.List;

/**
 * Six acts. The partner project, Lazy Load, built a session-closed exception
 * by hand. Here Hibernate raises its own, on purpose, and every statement
 * count comes from Hibernate's statistics.
 */
public final class LazyHibernateDemo {

    public static void main(String[] args) {
        System.out.println("LAZY LOAD WITH HIBERNATE — the exception everybody has met\n");

        SessionFactory factory = HibernateSetup.seeded();
        try {
            actOne(factory);
            actTwo(factory);
            actThree(factory);
            actFour(factory);
            actFive(factory);
            actSix(factory);
        } finally {
            factory.close();
        }
    }

    private static void actOne(SessionFactory factory) {
        System.out.println("ONE. Load an order, close the session, use the customer.");
        List<CustomerOrder> orders = new OrderPage(factory).loadOrdersAndClose();
        CustomerOrder order = orders.get(0);
        System.out.println("  the order loaded fine: order " + order.id());
        try {
            order.customer().name();
        } catch (LazyInitializationException e) {
            System.out.println("  asking for the customer's name threw " + e.getClass().getSimpleName() + ":");
            System.out.println("  " + e.getMessage());
        }
        System.out.println("  the failure is where it was used, not where it was loaded.\n");
    }

    private static void actTwo(SessionFactory factory) {
        System.out.println("TWO. What is actually in the field.");
        try (Session session = factory.openSession()) {
            CustomerOrder order = session.find(CustomerOrder.class, 1);
            Customer customer = order.customer();
            System.out.println("  order.customer() is a " + (customer.getClass() == Customer.class ? "Customer" : "generated subclass of Customer")
                    + ", initialised: " + Hibernate.isInitialized(customer));
            System.out.println("  the proxy holds only the id (" + factory.getPersistenceUnitUtil().getIdentifier(customer)
                    + ") and a reference to the session. it has not loaded the customer.");
            customer.name();
            System.out.println("  after asking for the name, inside the session, initialised: " + Hibernate.isInitialized(customer));
        }
        System.out.println("  when the session closes, the proxy has nothing to load with. that is the exception.\n");
    }

    private static void actThree(SessionFactory factory) {
        System.out.println("THREE. Fix one: keep the session open.");
        HibernateSetup.clearCount(factory);
        List<String> names = new OrderPage(factory).renderWithSessionOpen();
        System.out.println("  " + names.size() + " orders, each with its customer's name: " + HibernateSetup.statements(factory)
                + " statements. one for the orders, then one for each of the 5 distinct customers,");
        System.out.println("  because the session loads each customer once. the identity map, again.");
        HibernateSetup.clearCount(factory);
        List<String> counts = new OrderPage(factory).renderLineCountsWithSessionOpen();
        System.out.println("  " + counts.size() + " orders, each with its line count: " + HibernateSetup.statements(factory)
                + " statements. one for the orders, then one for each order's lines. that is N+1.");
        System.out.println("  it works. the cost: the session, and its connection, stay open while the page renders,");
        System.out.println("  and the extra queries are hidden inside the view, where nobody looks.\n");
    }

    private static void actFour(SessionFactory factory) {
        System.out.println("FOUR. Fix two: fetch it in the same query.");
        HibernateSetup.clearCount(factory);
        List<String> names = new OrderPage(factory).renderWithJoinFetch();
        System.out.println("  join fetch of the customer: " + names.size() + " orders, " + HibernateSetup.statements(factory) + " statement.");
        HibernateSetup.clearCount(factory);
        List<String> counts = new OrderPage(factory).renderLineCountsWithJoinFetch();
        System.out.println("  join fetch of the lines:    " + counts.size() + " orders, " + HibernateSetup.statements(factory) + " statement.");
        System.out.println("  the cost: that one statement makes the database send " + new OrderPage(factory).rowsTheJoinProduces()
                + " rows for 20 orders,");
        System.out.println("  each order repeated once per line, and Hibernate folds them back together. and every caller");
        System.out.println("  of this query now gets the lines, wanted or not.\n");
    }

    private static void actFive(SessionFactory factory) {
        System.out.println("FIVE. Fix three: ask for exactly what the page needs.");
        HibernateSetup.clearCount(factory);
        List<OrderPage.OrderRow> rows = new OrderPage(factory).renderWithProjection();
        System.out.println("  projection: " + rows.size() + " rows, " + HibernateSetup.statements(factory)
                + " statement, first row " + rows.get(0));
        System.out.println("  no entity, no proxy, nothing lazy to fail. the cost: a class for every query,");
        System.out.println("  and a row is not an object with behaviour. this is the DTO project's idea.\n");
    }

    private static void actSix(SessionFactory factory) {
        System.out.println("SIX. Where you have already met this.");
        System.out.println("  that exception is one of the most searched Java errors there is.");
        System.out.println("  now you know its mechanism: a proxy, and a session that has gone.");
        System.out.println("  making the mapping eager would remove it, and bring back the partner's act one.");
    }
}
