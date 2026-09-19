package com.jk.explore.unitofworkspring.service;

import com.jk.explore.unitofworkspring.domain.Product;
import com.jk.explore.unitofworkspring.domain.OrderLine;
import com.jk.explore.unitofworkspring.domain.StockFailure;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * <strong>One annotation is the unit of work.</strong> Every change made
 * inside the method is written when the method returns, or none of them are if
 * an unchecked exception leaves it.
 */
@Service
public class TransactionalPlacement {

    @PersistenceContext
    private EntityManager em;

    @Transactional
    public void place() {
        em.persist(Shelf.newOrder());
        int lineNo = 1;
        for (int[] line : Shelf.orderLines()) {
            if (line[0] == Shelf.FAILING_PRODUCT) {
                throw new StockFailure(line[0]);
            }
            em.find(Product.class, line[0]).take(line[1]);
            em.persist(new OrderLine(1000 + lineNo++, 100, line[0], line[1]));
        }
    }

    /** Succeeds, and reports what had been written to the database before, and after, the commit. */
    @Transactional
    public long[] placeGoodOrderReportingWrites(Shelf shelf) {
        em.persist(Shelf.newOrder());
        em.persist(new OrderLine(1001, 100, 1, 2));
        em.find(Product.class, 1).take(2);
        long insertsBefore = shelf.insertsIssued();
        long updatesBefore = shelf.updatesIssued();
        return new long[]{insertsBefore, updatesBefore};
    }
}
