package com.jk.explore.materializedview;

import java.util.ArrayList;
import java.util.List;

/**
 * The five acts: the page built by asking three services, the ready-made view, the lag, the rebuild, and the bill.
 */
public final class MaterializedViewDemo {

    public static void main(String[] args) {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** The shop's history so far: two product names and three orders from Priya, two shipped. */
    static List<Event> history() {
        return List.of(
                new Event.ProductRenamed("P-1", "kettle"),
                new Event.ProductRenamed("P-2", "teapot"),
                new Event.OrderPlaced("ORD-1", "C-17", "P-1", 1),
                new Event.OrderPlaced("ORD-2", "C-17", "P-2", 2),
                new Event.OrderPlaced("ORD-3", "C-17", "P-1", 1),
                new Event.OrderShipped("ORD-1"),
                new Event.OrderShipped("ORD-2"));
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() {
        List<String> out = new ArrayList<>();
        Services services = new Services();
        EventLog log = new EventLog();
        OrderHistoryView view = new OrderHistoryView();
        for (Event e : history()) {
            services.apply(e);
            log.publish(e);
        }

        out.add("ONE. Build the page by asking three services.");
        List<HistoryRow> page = new QueryOnRead(services).myOrders("C-17");
        page.forEach(r -> out.add("  " + r));
        out.add("  one page, 3 orders: " + services.calls() + " service calls, about "
                + services.calls() * Services.MS_PER_CALL + " ms of waiting");
        services.setCatalogueUp(false);
        try {
            new QueryOnRead(services).myOrders("C-17");
        } catch (IllegalStateException e) {
            out.add("  catalogue goes down: the page fails, " + e.getMessage());
        }

        out.add("");
        out.add("TWO. A ready-made view, kept up to date by events.");
        int delivered = log.deliver(view::on);
        out.add("  the view heard " + delivered + " events and wrote " + view.rowCount() + " rows");
        int before = services.calls();
        List<HistoryRow> fromView = view.myOrders("C-17");
        out.add("  page from the view: " + fromView.size() + " rows, "
                + (services.calls() - before) + " service calls, catalogue still down");
        out.add("  same page as before: " + fromView.equals(page));

        out.add("");
        out.add("THREE. The view is a moment behind.");
        Event shipped = new Event.OrderShipped("ORD-3");
        services.apply(shipped);
        log.publish(shipped);
        out.add("  ORD-3 ships; the event is on its way (" + log.waiting() + " waiting)");
        out.add("  page right now: " + view.myOrders("C-17").get(2));
        log.deliver(view::on);
        out.add("  a moment later: " + view.myOrders("C-17").get(2));

        out.add("");
        out.add("FOUR. Throw the view away and rebuild it.");
        OrderHistoryView rebuilt = new OrderHistoryView();
        log.history().forEach(rebuilt::on);
        out.add("  replayed " + log.history().size() + " events into an empty view");
        out.add("  rebuilt page equals the old one: " + rebuilt.myOrders("C-17").equals(view.myOrders("C-17")));

        out.add("");
        out.add("FIVE. The bill: a copy to keep in step.");
        Event rename = new Event.ProductRenamed("P-1", "steel kettle");
        services.apply(rename);
        log.publish(rename);
        log.deliver(view::on);
        out.add("  kettle renamed: the catalogue changed 1 name; the view rewrote "
                + view.rowsRewritten() + " rows");
        out.add("  " + view.rowCount() + " rows stored that the three services already hold");
        out.add("  and every page it serves may be a moment out of date");
        return out;
    }

    private MaterializedViewDemo() {
    }
}
