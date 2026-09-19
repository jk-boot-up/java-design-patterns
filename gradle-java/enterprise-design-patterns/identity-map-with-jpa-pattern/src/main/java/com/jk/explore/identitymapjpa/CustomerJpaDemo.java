package com.jk.explore.identitymapjpa;

import com.jk.explore.identitymapjpa.domain.Customer;
import com.jk.explore.identitymapjpa.domain.CustomerOrder;
import jakarta.persistence.EntityManager;
import jakarta.persistence.EntityManagerFactory;
import org.hibernate.Session;

/**
 * Six acts. The partner project, Identity Map, built this mechanism by hand.
 * Here the same customer 7 and order 100 go through the real thing, and every
 * SQL count comes from Hibernate's own statistics.
 */
public final class CustomerJpaDemo {

    public static void main(String[] args) {
        System.out.println("IDENTITY MAP WITH JPA — the persistence context is the map\n");

        actOne();
        actTwo();
        actThree();
        actFour();
        actFive();
        actSix();
    }

    private static void actOne() {
        System.out.println("ONE. Load the same customer twice in one persistence context.");
        EntityManagerFactory emf = JpaSetup.seeded();
        try (EntityManager em = emf.createEntityManager()) {
            Customer first = em.find(Customer.class, 7);
            Customer second = em.find(Customer.class, 7);
            System.out.println("  first == second: " + (first == second));
            System.out.println("  SQL statements issued: " + JpaSetup.sqlStatements(emf));
            System.out.println("  this is the identity map from the last project, and you did not write it.\n");
        }
        emf.close();
    }

    private static void actTwo() {
        System.out.println("TWO. The order's customer and customer 7 by id.");
        EntityManagerFactory emf = JpaSetup.seeded();
        try (EntityManager em = emf.createEntityManager()) {
            CustomerOrder order = em.find(CustomerOrder.class, 100);
            Customer direct = em.find(Customer.class, 7);
            System.out.println("  the order's customer == customer 7 by id: " + (order.customer() == direct));
            System.out.println("  SQL statements issued: " + JpaSetup.sqlStatements(emf) + " (the order and its customer, once)\n");
        }
        emf.close();
    }

    private static void actThree() {
        System.out.println("THREE. Two changes to one customer are both kept.");
        EntityManagerFactory emf = JpaSetup.seeded();
        try (EntityManager em = emf.createEntityManager()) {
            em.getTransaction().begin();
            Customer viaOrder = em.find(CustomerOrder.class, 100).customer();
            Customer direct = em.find(Customer.class, 7);
            viaOrder.moveTo("1 High Street, York");
            direct.changeEmail("ada@newmail.example");
            JpaSetup.clearCount(emf);
            em.getTransaction().commit();
            System.out.println("  one object moved her and changed her email. SQL statements at commit: "
                    + JpaSetup.sqlStatements(emf) + " (one UPDATE)");
        }
        try (EntityManager check = emf.createEntityManager()) {
            Customer stored = check.find(Customer.class, 7);
            System.out.println("  stored address: " + stored.address());
            System.out.println("  stored email:   " + stored.email());
            System.out.println("  nothing lost: there was only ever one object.\n");
        }
        emf.close();
    }

    private static void actFour() {
        System.out.println("FOUR. Two persistence contexts — two objects again.");
        EntityManagerFactory emf = JpaSetup.seeded();
        Customer fromFirst;
        Customer fromSecond;
        try (EntityManager one = emf.createEntityManager(); EntityManager two = emf.createEntityManager()) {
            fromFirst = one.find(Customer.class, 7);
            fromSecond = two.find(Customer.class, 7);
            System.out.println("  customer 7 from context one == from context two: " + (fromFirst == fromSecond));
            System.out.println("  equals: " + fromFirst.equals(fromSecond) + ". same customer, two objects, and each is free to disagree.");
        }
        System.out.println("  both contexts are now closed. the objects are detached.");
        fromFirst.moveTo("Nowhere in particular");
        try (EntityManager three = emf.createEntityManager()) {
            three.getTransaction().begin();
            Customer managed = three.find(Customer.class, 7);
            three.getTransaction().commit();
            System.out.println("  a detached customer was changed. stored address is still: " + managed.address());
        }
        System.out.println("  nothing tracks a detached object. the change is silently not saved.\n");
        emf.close();
    }

    private static void actFive() {
        System.out.println("FIVE. The context is a cache, so it can be stale.");
        EntityManagerFactory emf = JpaSetup.seeded();
        try (EntityManager em = emf.createEntityManager()) {
            Customer seen = em.find(Customer.class, 7);
            try (EntityManager other = emf.createEntityManager()) {
                other.getTransaction().begin();
                other.find(Customer.class, 7).changeEmail("ada@other.example");
                other.getTransaction().commit();
            }
            System.out.println("  another context committed a new email.");
            System.out.println("  this context still sees: " + em.find(Customer.class, 7).email());
            em.refresh(seen);
            System.out.println("  after refresh it sees:   " + seen.email() + "\n");
        }
        emf.close();
    }

    private static void actSix() {
        System.out.println("SIX. It holds references, and its scope is a decision.");
        EntityManagerFactory emf = JpaSetup.seeded();
        try (EntityManager em = emf.createEntityManager()) {
            em.getTransaction().begin();
            for (int i = 1_000; i < 2_000; i++) {
                em.persist(new Customer(i, "Customer " + i, "c" + i + "@example.com", "Somewhere " + i));
            }
            em.getTransaction().commit();
            em.clear();
            for (int i = 1_000; i < 2_000; i++) {
                em.find(Customer.class, i);
            }
            Session session = em.unwrap(Session.class);
            System.out.println("  after loading 1000 customers, the context holds "
                    + session.getStatistics().getEntityCount() + " entities.");
            em.clear();
            System.out.println("  after clear(): " + session.getStatistics().getEntityCount() + ".");
            System.out.println("  in a Spring application, the context normally lives for one transaction or one request.");
        }
        emf.close();
    }
}
