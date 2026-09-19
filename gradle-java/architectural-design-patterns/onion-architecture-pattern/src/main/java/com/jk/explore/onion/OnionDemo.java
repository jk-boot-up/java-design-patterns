package com.jk.explore.onion;

import com.jk.explore.onion.application.PlaceOrderService;
import com.jk.explore.onion.domain.model.Order;
import com.jk.explore.onion.domain.model.OrderLine;
import com.jk.explore.onion.domain.model.OrderRepository;
import com.jk.explore.onion.domain.service.PricingService;
import com.jk.explore.onion.infrastructure.InMemoryOrderRepository;
import com.jk.explore.onion.infrastructure.RecordOrderRepository;
import com.jk.explore.onion.infrastructure.SqlDatabase;
import com.jk.explore.onion.naive.NaiveOrder;
import com.jk.explore.onion.ui.ConsoleApi;
import java.util.List;

public class OnionDemo {

    static final Class<?>[] GOOD = {Order.class, OrderLine.class, OrderRepository.class, PricingService.class,
            PlaceOrderService.class, InMemoryOrderRepository.class, RecordOrderRepository.class, ConsoleApi.class};

    public static void main(String[] args) {
        one();
        two();
        three();
        four();
        five();
        six();
    }

    private static void one() {
        System.out.println("ONE. The core reaches outward.");
        SqlDatabase db = new SqlDatabase();
        new NaiveOrder(db, 6000).save();
        System.out.println("  the order saved itself with a SQL statement. statements run: " + db.statements() + ".");
        System.out.println("  to change the storage, the order class, at the centre, must be edited.");
    }

    private static void two() {
        System.out.println("TWO. Rings, and one rule.");
        System.out.println("  ring 0: order, order line, the repository idea. ring 1: pricing rules. ring 2: use cases. ring 3: storage and screens.");
        System.out.println("  the rule: a class may refer to its own ring, or to a ring further in. never outward.");
        System.out.println("  violations among the 8 classes of the onion: " + DependencyRule.violations(GOOD).size() + ".");
    }

    private static void three() {
        System.out.println("THREE. Checking the rule.");
        List<String> v = DependencyRule.violations(NaiveOrder.class);
        System.out.println("  the naive order: " + v + ".");
        System.out.println("  the checker reads the fields, constructors and methods of each class, so the rule is tested, not just hoped for.");
    }

    private static void four() {
        System.out.println("FOUR. Swap the outside.");
        List<OrderLine> lines = List.of(new OrderLine("MUG", 2, 6000));
        InMemoryOrderRepository memory = new InMemoryOrderRepository();
        RecordOrderRepository records = new RecordOrderRepository();
        Order a = new PlaceOrderService(memory, new PricingService()).place("ORD-1", lines);
        Order b = new PlaceOrderService(records, new PricingService()).place("ORD-1", lines);
        System.out.println("  in memory: total " + a.totalCents() + ". as a text record: total " + b.totalCents() + ". the record: " + records.recordOf("ORD-1") + ".");
        System.out.println("  the use case, the rules and the order were not touched.");
    }

    private static void five() {
        System.out.println("FIVE. The inside, on its own.");
        Order small = new Order("ORD-2", List.of(new OrderLine("TEA", 1, 950)));
        Order big = new Order("ORD-3", List.of(new OrderLine("MUG", 2, 6000)));
        new PricingService().price(small);
        new PricingService().price(big);
        System.out.println("  small order total: " + small.totalCents() + ". big order total: " + big.totalCents() + " (10% off 12000).");
        System.out.println("  no storage, no screen, no framework was used to check the rules.");
        System.out.println("  through the outside, the same order: " + new ConsoleApi(new PlaceOrderService(new InMemoryOrderRepository(), new PricingService())).handle("ORD-3 MUG 2 6000") + ".");
    }

    private static void six() {
        System.out.println("SIX. The bill.");
        RecordOrderRepository records = new RecordOrderRepository();
        PlaceOrderService service = new PlaceOrderService(records, new PricingService());
        service.place("ORD-1", List.of(new OrderLine("MUG", 2, 6000)));
        records.find("ORD-1");
        System.out.println("  one order saved and read back through the outer ring: conversions " + records.conversions() + ". every trip across a ring may copy the order into another shape.");
        System.out.println("  and to place one order there are 4 classes in 3 rings, plus the repository idea. for a small program, that is a lot of ceremony.");
        System.out.println("  the repository idea lives in the centre, so the centre knows that storage exists, though not how.");
    }
}
