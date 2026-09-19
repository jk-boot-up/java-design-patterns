package com.jk.explore.lazyloadhibernate;

import com.jk.explore.lazyloadhibernate.domain.Customer;
import com.jk.explore.lazyloadhibernate.domain.CustomerOrder;
import org.hibernate.Hibernate;
import org.hibernate.LazyInitializationException;
import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotSame;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class LazyLoadHibernateTest {

    private SessionFactory factory;

    @BeforeEach
    void setUp() {
        factory = HibernateSetup.seeded();
    }

    @AfterEach
    void tearDown() {
        factory.close();
    }

    @Test
    void usingALazyFieldAfterTheSessionClosesThrowsLazyInitializationException() {
        CustomerOrder order = new OrderPage(factory).loadOrdersAndClose().get(0);
        assertEquals(1, order.id(), "the order itself loaded fine");
        LazyInitializationException e = assertThrows(LazyInitializationException.class, () -> order.customer().name());
        assertTrue(e.getMessage().contains("no session"), e.getMessage());
    }

    @Test
    void theLazyFieldHoldsAProxyThatIsInitialisedOnlyOnFirstUse() {
        try (Session session = factory.openSession()) {
            Customer customer = session.find(CustomerOrder.class, 1).customer();
            assertNotSame(Customer.class, customer.getClass(), "a generated subclass, not a Customer");
            assertFalse(Hibernate.isInitialized(customer));
            assertEquals(1, factory.getPersistenceUnitUtil().getIdentifier(customer), "the proxy knows its id without loading");
            assertFalse(Hibernate.isInitialized(customer));
            customer.name();
            assertTrue(Hibernate.isInitialized(customer));
        }
    }

    @Test
    void keepingTheSessionOpenWorksAndCostsOnePerDistinctCustomer() {
        HibernateSetup.clearCount(factory);
        assertEquals(20, new OrderPage(factory).renderWithSessionOpen().size());
        assertEquals(6, HibernateSetup.statements(factory), "one for the orders, one for each of 5 customers");
    }

    @Test
    void lazyLineCountsCostNPlusOne() {
        HibernateSetup.clearCount(factory);
        List<String> page = new OrderPage(factory).renderLineCountsWithSessionOpen();
        assertEquals(20, page.size());
        assertEquals(21, HibernateSetup.statements(factory));
    }

    @Test
    void joinFetchIsOneStatementForEitherPage() {
        HibernateSetup.clearCount(factory);
        assertEquals(20, new OrderPage(factory).renderWithJoinFetch().size());
        assertEquals(1, HibernateSetup.statements(factory));
        HibernateSetup.clearCount(factory);
        assertEquals(20, new OrderPage(factory).renderLineCountsWithJoinFetch().size());
        assertEquals(1, HibernateSetup.statements(factory));
    }

    @Test
    void theJoinFetchOfLinesSendsEightyRowsForTwentyOrders() {
        assertEquals(80, new OrderPage(factory).rowsTheJoinProduces());
    }

    @Test
    void aProjectionIsOneStatementAndNothingIsLazy() {
        HibernateSetup.clearCount(factory);
        List<OrderPage.OrderRow> rows = new OrderPage(factory).renderWithProjection();
        assertEquals(20, rows.size());
        assertEquals(1, HibernateSetup.statements(factory));
        assertEquals("Customer 1", rows.get(0).customerName());
    }
}
