package com.jk.explore.repositoryspringdata.service;

import com.jk.explore.repositoryspringdata.domain.Customer;
import com.jk.explore.repositoryspringdata.domain.CustomerOrder;
import com.jk.explore.repositoryspringdata.repository.CustomerRepository;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import org.hibernate.SessionFactory;
import org.hibernate.stat.Statistics;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

/** Seeds the partner's six customers, and counts statements. Today is day 100. */
@Component
public class Seeder {

    @PersistenceContext
    private EntityManager em;

    private final CustomerRepository customers;

    public Seeder(CustomerRepository customers) {
        this.customers = customers;
    }

    @Transactional
    public void reset() {
        em.createQuery("delete from CustomerOrder").executeUpdate();
        em.createQuery("delete from Customer").executeUpdate();
        Customer ada = add(1, "Ada", "London");
        order(ada, 1, 95, "SHIPPED");
        order(ada, 2, 40, "SHIPPED");
        Customer grace = add(2, "Grace", "London");
        order(grace, 3, 60, "PENDING");
        order(grace, 4, 99, "PENDING");
        Customer linus = add(3, "Linus", "Leeds");
        order(linus, 5, 98, "SHIPPED");
        Customer ken = add(4, "Ken", "London");
        order(ken, 6, 70, "SHIPPED");
        add(5, "Dennis", "Leeds");
        Customer barbara = add(6, "Barbara", "London");
        order(barbara, 7, 10, "SHIPPED");
        em.flush();
        statistics().clear();
    }

    private Customer add(int id, String name, String city) {
        return customers.save(new Customer(id, name, city));
    }

    private void order(Customer customer, int id, int day, String status) {
        CustomerOrder order = new CustomerOrder(id, day, status, customer);
        em.persist(order);
        customer.orders().add(order);
    }

    public Statistics statistics() {
        return em.getEntityManagerFactory().unwrap(SessionFactory.class).getStatistics();
    }

    public long statements() {
        return statistics().getPrepareStatementCount();
    }

    public void clearCount() {
        statistics().clear();
    }

    @Transactional(readOnly = true)
    public String cityOf(int id) {
        return em.find(Customer.class, id).city();
    }
}
