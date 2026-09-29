package com.jk.explore.messagefilter;

import java.util.ArrayList;
import java.util.List;

/**
 * The five acts: every receiver gets everything, a filter in front of one receiver, chained filters, a changed rule, and the bill.
 */
public final class MessageFilterDemo {

    static final List<OrderEvent> ORDERS = List.of(
            new OrderEvent("ORD-1", "Priya", true, 6400, false),
            new OrderEvent("ORD-2", "guest", false, 1200, true),
            new OrderEvent("ORD-3", "Tom", true, 2500, false),
            new OrderEvent("ORD-4", "Ana", true, 8900, true),
            new OrderEvent("ORD-5", "guest", false, 7200, false),
            new OrderEvent("ORD-6", "Priya", true, 5500, false),
            new OrderEvent("ORD-7", "Sam", true, 900, false),
            new OrderEvent("ORD-8", "guest", false, 300, false),
            new OrderEvent("ORD-9", "Tom", true, 4800, false),
            new OrderEvent("ORD-10", "Lee", true, 1500, false));

    public static void main(String[] args) {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() {
        List<String> out = new ArrayList<>();

        out.add("ONE. Every service is handed every order.");
        Channel c1 = new Channel();
        Services.GiftWrapUnfiltered giftWrap = new Services.GiftWrapUnfiltered();
        c1.subscribe(giftWrap);
        ORDERS.forEach(c1::send);
        out.add("  gift-wrap service handed " + giftWrap.handed() + " orders, wrapped " + giftWrap.wrapped());
        out.add("  " + (giftWrap.handed() - giftWrap.wrapped().size()) + " deliveries it had to open and ignore;"
                + " and every service repeats its own checks");

        out.add("");
        out.add("TWO. A message filter in front of the gift-wrap service.");
        Channel c2 = new Channel();
        Services.Receiver wrap = new Services.Receiver();
        MessageFilter giftsOnly = new MessageFilter("gift orders only", OrderEvent::gift, wrap);
        c2.subscribe(giftsOnly);
        ORDERS.forEach(c2::send);
        out.add("  gift-wrap service receives: " + wrap.received() + "; the filter dropped " + giftsOnly.dropped());
        out.add("  checkout still just sends every order; it does not know the filter exists");

        out.add("");
        out.add("THREE. Filters chain: registered customers, orders over £50.");
        Channel c3 = new Channel();
        Services.Receiver loyalty = new Services.Receiver();
        MessageFilter over50 = new MessageFilter("over £50", e -> e.pence() > 5000, loyalty);
        MessageFilter registered = new MessageFilter("registered customers", OrderEvent::registered, over50);
        c3.subscribe(registered);
        ORDERS.forEach(c3::send);
        out.add("  loyalty bonus service receives: " + loyalty.received());
        out.add("  dropped: " + registered.dropped() + " guests, then " + over50.dropped() + " under £50");

        out.add("");
        out.add("FOUR. The rule changes; nothing else does.");
        Channel c4 = new Channel();
        Services.Receiver loyalty2 = new Services.Receiver();
        c4.subscribe(new MessageFilter("registered", OrderEvent::registered,
                new MessageFilter("over £60", e -> e.pence() > 6000, loyalty2)));
        ORDERS.forEach(c4::send);
        out.add("  bonus threshold raised to £60: " + loyalty2.received());
        out.add("  checkout and the loyalty service were not changed");

        out.add("");
        out.add("FIVE. The bill: a dropped message is gone.");
        out.add("  " + (giftsOnly.dropped() + registered.dropped() + over50.dropped())
                + " messages were dropped by the filters above; none of them was kept anywhere");
        out.add("  a wrong rule drops orders silently: count the drops, or send them to a discard channel");
        return out;
    }

    private MessageFilterDemo() {
    }
}
