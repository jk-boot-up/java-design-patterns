package com.jk.explore.lazyload;

import com.jk.explore.lazyload.domain.Shop;
import com.jk.explore.lazyload.naive.EagerOrderLoader;
import com.jk.explore.lazyload.pattern.CustomerProxy;
import com.jk.explore.lazyload.pattern.GhostCustomer;
import com.jk.explore.lazyload.pattern.LazyInitOrder;
import com.jk.explore.lazyload.pattern.OrderList;
import com.jk.explore.lazyload.pattern.Session;
import com.jk.explore.lazyload.pattern.SessionClosedException;
import com.jk.explore.lazyload.pattern.ValueHolder;
import com.jk.explore.lazyload.toydb.Database;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class LazyLoadTest {

    @Test
    void eagerLoadingOneOrderCreatesThirtySevenObjects() {
        Database db = Shop.seeded();
        assertEquals(37, new EagerOrderLoader(db).load(1));
        assertEquals(26, db.operationCount());
    }

    @Test
    void lazyInitialisationLoadsOnceOnFirstUse() {
        Database db = Shop.seeded();
        LazyInitOrder order = new LazyInitOrder(new Session(db), 1);
        assertEquals(0, db.operationCount());
        assertEquals("Customer 1", order.customerName());
        order.customerName();
        assertEquals(1, db.operationCount());
    }

    @Test
    void aVirtualProxyLoadsOnceOnFirstUse() {
        Database db = Shop.seeded();
        CustomerProxy proxy = new CustomerProxy(new Session(db), 2);
        assertEquals(0, db.operationCount());
        proxy.name();
        proxy.name();
        assertEquals(1, db.operationCount());
    }

    @Test
    void aValueHolderLoadsOnceOnFirstUse() {
        Database db = Shop.seeded();
        Session session = new Session(db);
        ValueHolder<String> holder = new ValueHolder<>(() -> session.select(Shop.CUSTOMERS, 3).text("name"));
        assertEquals(0, db.operationCount());
        assertEquals("Customer 3", holder.value());
        holder.value();
        assertEquals(1, db.operationCount());
    }

    @Test
    void aGhostKnowsItsIdAndLoadsEverythingElseOnFirstAccess() {
        Database db = Shop.seeded();
        GhostCustomer ghost = new GhostCustomer(new Session(db), 4);
        assertEquals(4, ghost.id());
        assertEquals(0, db.operationCount(), "asking for the id needs no load");
        assertEquals("Customer 4", ghost.name());
        assertEquals(1, db.operationCount());
    }

    @Test
    void aPageOfTwentyOrdersCostsTwentyOneLazyQueriesAndTwoBatched() {
        Database db = Shop.seeded();
        assertEquals(20, new OrderList(db).lazy().size());
        assertEquals(21, db.operationCount());
        db.clearLog();
        assertEquals(new OrderList(db).lazy(), new OrderList(db).batched(), "same page either way");
        Database db2 = Shop.seeded();
        new OrderList(db2).batched();
        assertEquals(2, db2.operationCount());
    }

    @Test
    void aFieldAccessCanFailBecauseItIsARead() {
        Database db = Shop.seeded();
        CustomerProxy proxy = new CustomerProxy(new Session(db), 1);
        db.failReadNumber(1);
        assertThrows(IllegalStateException.class, proxy::name);
    }

    @Test
    void aClosedSessionFailsAtTheMomentOfUseNotOfCreation() {
        Database db = Shop.seeded();
        Session session = new Session(db);
        CustomerProxy proxy = new CustomerProxy(session, 1);
        session.close();
        SessionClosedException e = assertThrows(SessionClosedException.class, proxy::name);
        assertTrue(e.getMessage().contains("closed"));
    }

    @Test
    void aProxyLoadedBeforeTheSessionClosedStillWorksAfter() {
        Session session = new Session(Shop.seeded());
        CustomerProxy proxy = new CustomerProxy(session, 1);
        proxy.name();
        session.close();
        assertEquals("Customer 1", proxy.name());
    }
}
