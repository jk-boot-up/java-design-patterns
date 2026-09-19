package com.jk.explore.lazyloadhibernate;

import com.jk.explore.lazyloadhibernate.domain.Category;
import com.jk.explore.lazyloadhibernate.domain.Customer;
import com.jk.explore.lazyloadhibernate.domain.CustomerOrder;
import com.jk.explore.lazyloadhibernate.domain.OrderLine;
import com.jk.explore.lazyloadhibernate.domain.Product;
import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.hibernate.cfg.Configuration;

import java.util.UUID;

/**
 * Builds a Hibernate {@code SessionFactory} over in-memory H2 and seeds the
 * partner's store: 5 customers, 20 orders, 4 lines per order, 12 products and
 * 4 categories. Statistics are on, so every statement can be counted.
 */
public final class HibernateSetup {

    static {
        java.util.logging.Logger.getLogger("org.hibernate").setLevel(java.util.logging.Level.SEVERE);
    }

    private HibernateSetup() {
    }

    public static SessionFactory seeded() {
        SessionFactory factory = new Configuration()
                .addAnnotatedClass(Category.class).addAnnotatedClass(Product.class)
                .addAnnotatedClass(Customer.class).addAnnotatedClass(CustomerOrder.class)
                .addAnnotatedClass(OrderLine.class)
                .setProperty("jakarta.persistence.jdbc.url", "jdbc:h2:mem:" + UUID.randomUUID() + ";DB_CLOSE_DELAY=-1")
                .setProperty("hibernate.hbm2ddl.auto", "create-drop")
                .setProperty("hibernate.generate_statistics", "true")
                .buildSessionFactory();
        try (Session session = factory.openSession()) {
            session.beginTransaction();
            Category[] categories = new Category[4];
            for (int c = 0; c < 4; c++) {
                categories[c] = new Category(c + 1, "Category " + (c + 1));
                session.persist(categories[c]);
            }
            Product[] products = new Product[12];
            for (int p = 0; p < 12; p++) {
                products[p] = new Product(p + 1, "Product " + (p + 1), categories[p % 4]);
                session.persist(products[p]);
            }
            Customer[] customers = new Customer[5];
            for (int c = 0; c < 5; c++) {
                customers[c] = new Customer(c + 1, "Customer " + (c + 1));
                session.persist(customers[c]);
            }
            int line = 1;
            for (int o = 1; o <= 20; o++) {
                CustomerOrder order = new CustomerOrder(o, customers[(o - 1) / 4]);
                session.persist(order);
                for (int l = 0; l < 4; l++) {
                    OrderLine orderLine = new OrderLine(line, order, products[(line - 1) % 12], 1);
                    order.lines().add(orderLine);
                    session.persist(orderLine);
                    line++;
                }
            }
            session.getTransaction().commit();
        }
        factory.getStatistics().clear();
        return factory;
    }

    public static long statements(SessionFactory factory) {
        return factory.getStatistics().getPrepareStatementCount();
    }

    public static void clearCount(SessionFactory factory) {
        factory.getStatistics().clear();
    }
}
