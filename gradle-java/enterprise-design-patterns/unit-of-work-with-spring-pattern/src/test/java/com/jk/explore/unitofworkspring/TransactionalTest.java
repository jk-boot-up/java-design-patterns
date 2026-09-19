package com.jk.explore.unitofworkspring;

import com.jk.explore.unitofworkspring.domain.StockFailure;
import com.jk.explore.unitofworkspring.domain.StockFailureChecked;
import com.jk.explore.unitofworkspring.service.CheckedFailurePlacement;
import com.jk.explore.unitofworkspring.service.FlushNobodyWrote;
import com.jk.explore.unitofworkspring.service.SelfInvocation;
import com.jk.explore.unitofworkspring.service.SelfSavingPlacement;
import com.jk.explore.unitofworkspring.service.Shelf;
import com.jk.explore.unitofworkspring.service.TransactionalPlacement;
import jakarta.persistence.TransactionRequiredException;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

@SpringBootTest(classes = OrderApplication.class, properties = "spring.datasource.url=jdbc:h2:mem:tx-test;DB_CLOSE_DELAY=-1")
class TransactionalTest {

    @Autowired Shelf shelf;
    @Autowired SelfSavingPlacement selfSaving;
    @Autowired TransactionalPlacement transactional;
    @Autowired CheckedFailurePlacement checked;
    @Autowired FlushNobodyWrote flush;
    @Autowired SelfInvocation selfInvocation;

    @BeforeEach
    void reset() {
        shelf.reset();
    }

    @Test
    void withoutATransactionAroundTheOrderHalfOfItIsCommitted() {
        assertThrows(StockFailure.class, selfSaving::place);
        assertEquals(new Shelf.Committed(1, 2, 8, 9, 10), shelf.committed());
    }

    @Test
    void transactionalWritesNothingUntilTheMethodReturns() {
        long[] beforeCommit = transactional.placeGoodOrderReportingWrites(shelf);
        assertEquals(0, beforeCommit[0], "no INSERT written inside the method");
        assertEquals(0, beforeCommit[1], "no UPDATE written inside the method");
        assertEquals(2, shelf.insertsIssued());
        assertEquals(1, shelf.updatesIssued());
    }

    @Test
    void anUncheckedExceptionRollsTheWholeOrderBack() {
        assertThrows(StockFailure.class, transactional::place);
        assertEquals(new Shelf.Committed(0, 0, 10, 10, 10), shelf.committed());
    }

    @Test
    void aCheckedExceptionCommitsHalfTheOrderAnyway() {
        assertThrows(StockFailureChecked.class, checked::place);
        assertEquals(new Shelf.Committed(1, 2, 8, 9, 10), shelf.committed());
    }

    @Test
    void rollbackForMakesTheCheckedExceptionRollBack() {
        assertThrows(StockFailureChecked.class, checked::placeWithRollbackFor);
        assertEquals(new Shelf.Committed(0, 0, 10, 10, 10), shelf.committed());
    }

    @Test
    void aQueryMakesHibernateWriteTheChangeBeforeTheCommit() {
        long[] updates = flush.changeThenQuery(shelf);
        assertEquals(0, updates[0]);
        assertEquals(0, updates[1], "held back after the change");
        assertEquals(1, updates[2], "written when the query ran");
    }

    @Test
    void aCallOnThisSkipsTheProxySoTheAnnotationIsNeverSeen() {
        assertThrows(TransactionRequiredException.class, selfInvocation::placeViaThis);
        assertEquals(new Shelf.Committed(1, 0, 10, 10, 10), shelf.committed());
    }
}
