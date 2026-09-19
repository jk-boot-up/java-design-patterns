package com.jk.explore.identitymapjpa;

import com.jk.explore.identitymapjpa.domain.Customer;
import com.jk.explore.identitymapjpa.domain.CustomerOrder;
import jakarta.persistence.EntityManager;
import jakarta.persistence.EntityManagerFactory;
import org.hibernate.SessionFactory;
import org.hibernate.cfg.Configuration;

import java.util.UUID;

/**
 * Builds a Hibernate {@code EntityManagerFactory} over an in-memory H2 database,
 * and seeds the same customer 7 and order 100 as the Identity Map project.
 * Statistics are switched on so every SQL statement can be counted.
 */
public final class JpaSetup {

    static {
        // Hibernate logs its start-up to standard error; keep the demo's output to what it means to say.
        java.util.logging.Logger.getLogger("org.hibernate").setLevel(java.util.logging.Level.SEVERE);
    }

    private JpaSetup() {
    }

    public static EntityManagerFactory seeded() {
        SessionFactory factory = new Configuration()
                .addAnnotatedClass(Customer.class)
                .addAnnotatedClass(CustomerOrder.class)
                .setProperty("jakarta.persistence.jdbc.url", "jdbc:h2:mem:" + UUID.randomUUID() + ";DB_CLOSE_DELAY=-1")
                .setProperty("hibernate.hbm2ddl.auto", "create-drop")
                .setProperty("hibernate.generate_statistics", "true")
                .buildSessionFactory();
        EntityManager em = factory.createEntityManager();
        em.getTransaction().begin();
        Customer ada = new Customer(7, "Ada Lovelace", "ada@example.com", "12 Mill Lane, Leeds");
        em.persist(ada);
        em.persist(new CustomerOrder(100, ada));
        em.getTransaction().commit();
        em.close();
        factory.getStatistics().clear();
        return factory;
    }

    /** SQL statements prepared since the statistics were last cleared. */
    public static long sqlStatements(EntityManagerFactory factory) {
        return factory.unwrap(SessionFactory.class).getStatistics().getPrepareStatementCount();
    }

    public static void clearCount(EntityManagerFactory factory) {
        factory.unwrap(SessionFactory.class).getStatistics().clear();
    }
}
