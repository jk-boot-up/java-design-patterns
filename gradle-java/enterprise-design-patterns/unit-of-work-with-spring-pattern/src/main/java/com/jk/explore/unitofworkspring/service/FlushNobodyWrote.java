package com.jk.explore.unitofworkspring.service;

import com.jk.explore.unitofworkspring.domain.Product;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * <strong>A flush nobody wrote.</strong> Changes are held until commit, except
 * that running a query first makes Hibernate write pending changes so the
 * query sees them. The write happens at a line that says nothing about writing.
 */
@Service
public class FlushNobodyWrote {

    @PersistenceContext
    private EntityManager em;

    /** Returns the update count before the change, after the change, and after an unrelated query. */
    @Transactional
    public long[] changeThenQuery(Shelf shelf) {
        long before = shelf.updatesIssued();
        em.find(Product.class, 1).take(2);
        long afterChange = shelf.updatesIssued();
        em.createQuery("select count(p) from Product p where p.stock < 100", Long.class).getSingleResult();
        long afterQuery = shelf.updatesIssued();
        return new long[]{before, afterChange, afterQuery};
    }
}
