package com.jk.explore.unitofworkspring.service;

import com.jk.explore.unitofworkspring.domain.OrderLine;
import com.jk.explore.unitofworkspring.domain.Product;
import com.jk.explore.unitofworkspring.domain.StockFailureChecked;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * <strong>The exception nobody expected to matter.</strong> Spring's default is
 * to roll back on unchecked exceptions and errors, and to <em>commit</em> on
 * checked ones. The same failure, declared as a checked exception, commits
 * half an order.
 */
@Service
public class CheckedFailurePlacement {

    @PersistenceContext
    private EntityManager em;

    @Transactional
    public void place() throws StockFailureChecked {
        em.persist(Shelf.newOrder());
        int lineNo = 1;
        for (int[] line : Shelf.orderLines()) {
            if (line[0] == Shelf.FAILING_PRODUCT) {
                throw new StockFailureChecked(line[0]);
            }
            em.find(Product.class, line[0]).take(line[1]);
            em.persist(new OrderLine(1000 + lineNo++, 100, line[0], line[1]));
        }
    }

    /** The one-line fix: say that this checked exception must roll back. */
    @Transactional(rollbackFor = StockFailureChecked.class)
    public void placeWithRollbackFor() throws StockFailureChecked {
        place();
    }
}
