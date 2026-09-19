package com.jk.explore.identitymapjpa;

import com.jk.explore.identitymapjpa.domain.Customer;
import com.jk.explore.identitymapjpa.domain.CustomerOrder;
import jakarta.persistence.EntityManager;
import jakarta.persistence.EntityManagerFactory;
import org.hibernate.Session;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotSame;
import static org.junit.jupiter.api.Assertions.assertSame;

class PersistenceContextTest {

    private EntityManagerFactory emf;

    @BeforeEach
    void setUp() {
        emf = JpaSetup.seeded();
    }

    @AfterEach
    void tearDown() {
        emf.close();
    }

    @Test
    void twoFindsInOneContextGiveTheSameObjectAndOneStatement() {
        try (EntityManager em = emf.createEntityManager()) {
            Customer first = em.find(Customer.class, 7);
            Customer second = em.find(Customer.class, 7);
            assertSame(first, second);
            assertEquals(1, JpaSetup.sqlStatements(emf));
        }
    }

    @Test
    void theOrdersCustomerIsTheSameObjectAsCustomerSevenById() {
        try (EntityManager em = emf.createEntityManager()) {
            CustomerOrder order = em.find(CustomerOrder.class, 100);
            assertSame(order.customer(), em.find(Customer.class, 7));
        }
    }

    @Test
    void twoChangesToTheOneObjectAreBothSavedInOneUpdate() {
        try (EntityManager em = emf.createEntityManager()) {
            em.getTransaction().begin();
            Customer a = em.find(CustomerOrder.class, 100).customer();
            Customer b = em.find(Customer.class, 7);
            a.moveTo("1 High Street, York");
            b.changeEmail("ada@newmail.example");
            JpaSetup.clearCount(emf);
            em.getTransaction().commit();
            assertEquals(1, JpaSetup.sqlStatements(emf));
        }
        try (EntityManager check = emf.createEntityManager()) {
            Customer stored = check.find(Customer.class, 7);
            assertEquals("1 High Street, York", stored.address());
            assertEquals("ada@newmail.example", stored.email());
        }
    }

    @Test
    void twoContextsGiveTwoObjects() {
        try (EntityManager one = emf.createEntityManager(); EntityManager two = emf.createEntityManager()) {
            Customer a = one.find(Customer.class, 7);
            Customer b = two.find(Customer.class, 7);
            assertNotSame(a, b);
            assertEquals(a, b, "equal by id, and still two objects");
        }
    }

    @Test
    void aChangeToADetachedObjectIsSilentlyNotSaved() {
        Customer detached;
        try (EntityManager em = emf.createEntityManager()) {
            detached = em.find(Customer.class, 7);
        }
        detached.moveTo("Nowhere in particular");
        try (EntityManager em = emf.createEntityManager()) {
            em.getTransaction().begin();
            assertEquals("12 Mill Lane, Leeds", em.find(Customer.class, 7).address());
            em.getTransaction().commit();
        }
    }

    @Test
    void theContextIsAStaleCacheUntilRefreshed() {
        try (EntityManager em = emf.createEntityManager()) {
            Customer seen = em.find(Customer.class, 7);
            try (EntityManager other = emf.createEntityManager()) {
                other.getTransaction().begin();
                other.find(Customer.class, 7).changeEmail("ada@other.example");
                other.getTransaction().commit();
            }
            assertEquals("ada@example.com", em.find(Customer.class, 7).email());
            em.refresh(seen);
            assertEquals("ada@other.example", seen.email());
        }
    }

    @Test
    void theContextHoldsEveryLoadedEntityUntilCleared() {
        try (EntityManager em = emf.createEntityManager()) {
            em.getTransaction().begin();
            for (int i = 1_000; i < 1_200; i++) {
                em.persist(new Customer(i, "c" + i, "e", "a"));
            }
            em.getTransaction().commit();
            em.clear();
            for (int i = 1_000; i < 1_200; i++) {
                em.find(Customer.class, i);
            }
            Session session = em.unwrap(Session.class);
            assertEquals(200, session.getStatistics().getEntityCount());
            em.clear();
            assertEquals(0, session.getStatistics().getEntityCount());
        }
    }
}
