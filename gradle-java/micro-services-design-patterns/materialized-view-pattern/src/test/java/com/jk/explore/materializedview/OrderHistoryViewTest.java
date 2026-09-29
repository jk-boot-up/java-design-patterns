package com.jk.explore.materializedview;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.List;
import org.junit.jupiter.api.Test;

class OrderHistoryViewTest {

    private OrderHistoryView viewOf(List<Event> events) {
        OrderHistoryView v = new OrderHistoryView();
        events.forEach(v::on);
        return v;
    }

    @Test
    void buildsTheSamePageAsAskingTheServices() {
        Services s = new Services();
        MaterializedViewDemo.history().forEach(s::apply);
        assertEquals(new QueryOnRead(s).myOrders("C-17"), viewOf(MaterializedViewDemo.history()).myOrders("C-17"));
    }

    @Test
    void readingMakesNoServiceCalls() {
        Services s = new Services();
        MaterializedViewDemo.history().forEach(s::apply);
        viewOf(MaterializedViewDemo.history()).myOrders("C-17");
        assertEquals(0, s.calls());
    }

    @Test
    void askingTheServicesCostsOnePlusTwoCallsPerOrder() {
        Services s = new Services();
        MaterializedViewDemo.history().forEach(s::apply);
        new QueryOnRead(s).myOrders("C-17");
        assertEquals(7, s.calls());
    }

    @Test
    void shippingUpdatesTheRow() {
        OrderHistoryView v = viewOf(MaterializedViewDemo.history());
        v.on(new Event.OrderShipped("ORD-3"));
        assertEquals("shipped", v.myOrders("C-17").get(2).status());
    }

    @Test
    void renameRewritesEveryRowForThatProduct() {
        OrderHistoryView v = viewOf(MaterializedViewDemo.history());
        v.on(new Event.ProductRenamed("P-1", "steel kettle"));
        assertEquals(2, v.rowsRewritten());
        assertEquals("steel kettle", v.myOrders("C-17").get(0).product());
        assertEquals("teapot", v.myOrders("C-17").get(1).product());
    }

    @Test
    void undeliveredEventsLeaveTheViewBehind() {
        EventLog log = new EventLog();
        OrderHistoryView v = new OrderHistoryView();
        MaterializedViewDemo.history().forEach(log::publish);
        assertEquals(0, v.rowCount());
        log.deliver(v::on);
        assertEquals(3, v.rowCount());
    }

    @Test
    void unknownCustomerHasAnEmptyPage() {
        assertEquals(List.of(), viewOf(MaterializedViewDemo.history()).myOrders("C-99"));
    }
}
