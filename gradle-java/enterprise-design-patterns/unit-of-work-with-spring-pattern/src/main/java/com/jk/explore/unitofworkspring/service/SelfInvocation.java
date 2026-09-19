package com.jk.explore.unitofworkspring.service;

import com.jk.explore.unitofworkspring.domain.OrderLine;
import com.jk.explore.unitofworkspring.domain.Product;
import com.jk.explore.unitofworkspring.domain.StockFailure;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.transaction.support.TransactionTemplate;

/**
 * <strong>The annotation that does nothing.</strong> {@code @Transactional}
 * works because Spring wraps the bean in a proxy. A call from one method of the
 * bean to another goes straight to {@code this}, not through the proxy, so the
 * annotation on the second method is never seen.
 */
@Service
public class SelfInvocation {

    @PersistenceContext
    private EntityManager em;

    private final TransactionTemplate eachStep;

    public SelfInvocation(TransactionTemplate eachStep) {
        this.eachStep = eachStep;
    }

    /** Not transactional itself. It calls a method that is, through {@code this}. */
    public void placeViaThis() {
        eachStep.executeWithoutResult(s -> em.persist(Shelf.newOrder()));
        placeLines();
    }

    @Transactional
    public void placeLines() {
        int lineNo = 1;
        for (int[] line : Shelf.orderLines()) {
            if (line[0] == Shelf.FAILING_PRODUCT) {
                throw new StockFailure(line[0]);
            }
            em.find(Product.class, line[0]).take(line[1]);
            em.persist(new OrderLine(1000 + lineNo++, 100, line[0], line[1]));
        }
    }
}
