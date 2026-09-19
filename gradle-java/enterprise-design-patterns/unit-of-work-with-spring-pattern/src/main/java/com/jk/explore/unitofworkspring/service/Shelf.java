package com.jk.explore.unitofworkspring.service;

import com.jk.explore.unitofworkspring.domain.CustomerOrder;
import com.jk.explore.unitofworkspring.domain.OrderLine;
import com.jk.explore.unitofworkspring.domain.Product;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import org.hibernate.SessionFactory;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

/** Seeds the store, resets it between acts, and reads what is really committed. */
@Component
public class Shelf {

    /** The product whose stock update fails: the third line of every order. */
    public static final int FAILING_PRODUCT = 3;

    @PersistenceContext
    private EntityManager em;

    @Transactional
    public void reset() {
        em.createQuery("delete from OrderLine").executeUpdate();
        em.createQuery("delete from CustomerOrder").executeUpdate();
        em.createQuery("delete from Product").executeUpdate();
        em.persist(new Product(1, "Keyboard", 10));
        em.persist(new Product(2, "Mouse", 10));
        em.persist(new Product(3, "Monitor", 10));
        em.flush();
        em.unwrap(org.hibernate.Session.class).getSessionFactory().getStatistics().clear();
    }

    /** Placing an order asks for one of each. The lines are (product 1, qty 2), (2, 1), (3, 1). */
    public static List<int[]> orderLines() {
        return List.of(new int[]{1, 2}, new int[]{2, 1}, new int[]{3, 1});
    }

    @Transactional(readOnly = true)
    public Committed committed() {
        long orders = em.createQuery("select count(o) from CustomerOrder o", Long.class).getSingleResult();
        long lines = em.createQuery("select count(l) from OrderLine l", Long.class).getSingleResult();
        int keyboard = em.find(Product.class, 1).stock();
        int mouse = em.find(Product.class, 2).stock();
        int monitor = em.find(Product.class, 3).stock();
        return new Committed(orders, lines, keyboard, mouse, monitor);
    }

    public record Committed(long orders, long lines, int keyboard, int mouse, int monitor) {
        public String describe() {
            return "orders " + orders + ", lines " + lines + ", stock keyboard " + keyboard + ", mouse " + mouse + ", monitor " + monitor;
        }
    }

    public long insertsIssued() {
        return statistics().getEntityInsertCount();
    }

    public long updatesIssued() {
        return statistics().getEntityUpdateCount();
    }

    private org.hibernate.stat.Statistics statistics() {
        return em.getEntityManagerFactory().unwrap(SessionFactory.class).getStatistics();
    }

    void placeStep(EntityManager em, int orderId, int lineNo, int productId, int quantity) {
        Product product = em.find(Product.class, productId);
        if (productId == FAILING_PRODUCT) {
            throw new com.jk.explore.unitofworkspring.domain.StockFailure(productId);
        }
        product.take(quantity);
        em.persist(new OrderLine(orderId * 10 + lineNo, orderId, productId, quantity));
    }

    static CustomerOrder newOrder() {
        return new CustomerOrder(100, 7);
    }
}
