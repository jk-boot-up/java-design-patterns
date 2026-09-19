package com.jk.explore.unitofworkspring.service;

import com.jk.explore.unitofworkspring.domain.CustomerOrder;
import com.jk.explore.unitofworkspring.domain.OrderLine;
import com.jk.explore.unitofworkspring.domain.Product;
import com.jk.explore.unitofworkspring.domain.StockFailure;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import org.springframework.stereotype.Service;
import org.springframework.transaction.support.TransactionTemplate;

/**
 * <strong>No transaction around the whole thing:</strong> every step commits
 * on its own, so a failure leaves whatever had already been committed. This
 * is the partner project's first act, through Spring.
 */
@Service
public class SelfSavingPlacement {

    @PersistenceContext
    private EntityManager em;

    private final TransactionTemplate eachStep;

    public SelfSavingPlacement(TransactionTemplate eachStep) {
        this.eachStep = eachStep;
    }

    public void place() {
        eachStep.executeWithoutResult(s -> em.persist(Shelf.newOrder()));
        int lineNo = 1;
        for (int[] line : Shelf.orderLines()) {
            int productId = line[0];
            int quantity = line[1];
            int number = lineNo++;
            eachStep.executeWithoutResult(s -> {
                if (productId == Shelf.FAILING_PRODUCT) {
                    throw new StockFailure(productId);
                }
                em.find(Product.class, productId).take(quantity);
                em.persist(new OrderLine(100 * 10 + number, 100, productId, quantity));
            });
        }
    }
}
