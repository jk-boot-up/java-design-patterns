package com.jk.explore.contextmap;

import com.jk.explore.contextmap.before.Separate;
import com.jk.explore.contextmap.kernel.Address;
import com.jk.explore.contextmap.sales.Sales;
import com.jk.explore.contextmap.shipping.Shipping;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

/**
 * The five acts: two copies of an address, a shared kernel, the context map, the map checked against the code, and the bill.
 */
public final class ContextMapDemo {

    static final Path SOURCES = Path.of("src/main/java/com/jk/explore/contextmap");

    public static void main(String[] args) {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() {
        List<String> out = new ArrayList<>();

        out.add("ONE. Sales and shipping each keep their own address.");
        Separate.SalesAddress typed = new Separate.SalesAddress("Flat 2", "4 Mill Lane", "Leeds");
        out.add("  Priya types: Flat 2, 4 Mill Lane, Leeds");
        out.add("  shipping label after the converter: " + Separate.convert(typed).label());
        out.add("  the flat number was lost between the two contexts; the parcel waits at the main door");

        out.add("");
        out.add("TWO. A shared kernel: one Address and one Money, used by both.");
        Address address = new Address("Flat 2", "4 Mill Lane", "Leeds");
        Sales.Order order = Sales.placeOrder("ORD-1", address, "KETTLE-1", "MUG-1");
        out.add("  sales: " + order.id() + " for " + order.total());
        out.add("  shipping: " + Shipping.label("PARCEL-1", order.deliverTo(), order.total()));
        out.add("  no converter: the same Address travels from sales to shipping");

        out.add("");
        out.add("THREE. The context map: who depends on whom, and how.");
        ContextMap.RELATIONSHIPS.forEach(r -> out.add("  " + r));
        out.add("  shipping does not know sales exists; it only knows the kernel");

        out.add("");
        out.add("FOUR. The map is checked against the code.");
        out.add("  imports the map does not allow: " + ContextMap.surprises(SOURCES).size());
        String shortcut = "import com.jk.explore.contextmap.sales.Sales;";
        out.add("  someone adds to shipping: " + shortcut);
        out.add("  check: " + ContextMap.check("shipping", "Shipping.java", shortcut).get(0));

        out.add("");
        out.add("FIVE. The bill: a kernel is shared, so it changes slowly.");
        out.add("  adding a postcode to Address needs both teams to agree, test and release together");
        out.add("  keep the kernel tiny: here 2 classes; everything else stays inside its own context");
        return out;
    }

    private ContextMapDemo() {
    }
}
