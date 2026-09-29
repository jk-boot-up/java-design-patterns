package com.jk.explore.modularmonolith;

import com.jk.explore.modularmonolith.catalog.CatalogApi;
import com.jk.explore.modularmonolith.mud.MudCheckout;
import com.jk.explore.modularmonolith.mud.Tables;
import com.jk.explore.modularmonolith.orders.OrdersApi;
import com.jk.explore.modularmonolith.payments.PaymentsApi;
import com.jk.explore.modularmonolith.payments.RemotePayments;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

/**
 * The five acts: the ball of mud, modules with front doors, the boundary check, moving a module out, and the bill.
 */
public final class ModularMonolithDemo {

    static final Path SOURCES = Path.of("src/main/java/com/jk/explore/modularmonolith");

    public static void main(String[] args) {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() {
        List<String> out = new ArrayList<>();

        out.add("ONE. One program, every table open to everyone.");
        Tables.STOCK.clear();
        Tables.PAYMENTS.clear();
        Tables.STOCK.put("kettle", 1);
        MudCheckout.placeOrder("ORD-1", "kettle", 1, 3000);
        MudCheckout.placeOrder("ORD-2", "kettle", 1, 3000);
        out.add("  1 kettle in stock; checkout writes the stock table itself, twice");
        out.add("  kettle stock is now " + Tables.STOCK.get("kettle") + "; two customers paid for one kettle");

        out.add("");
        out.add("TWO. Modules, each with a front door.");
        CatalogApi catalog = CatalogApi.create();
        PaymentsApi payments = PaymentsApi.create();
        OrdersApi orders = OrdersApi.create(catalog, payments);
        out.add("  " + orders.placeOrder("ORD-1", "kettle", 1, 3000));
        out.add("  " + orders.placeOrder("ORD-2", "kettle", 1, 3000));
        out.add("  kettle stock: " + catalog.stock("kettle") + "; the catalogue's rule holds, because only it can change stock");

        out.add("");
        out.add("THREE. The boundaries are checked, not hoped for.");
        out.add("  scan of this project's source: " + BoundaryCheck.scan(SOURCES).size() + " modules reaching inside another");
        String sneaky = "import com.jk.explore.modularmonolith.payments.internal.PaymentsModule;";
        out.add("  someone adds to OrdersModule: " + sneaky.substring(7, sneaky.length() - 1));
        out.add("  check says: " + BoundaryCheck.check("orders", "OrdersModule.java", sneaky) + ", and the build fails");

        out.add("");
        out.add("FOUR. Moving payments out into its own service.");
        RemotePayments remote = new RemotePayments();
        OrdersApi orders2 = OrdersApi.create(CatalogApi.create(), remote);
        out.add("  " + orders2.placeOrder("ORD-3", "mug", 2, 2000));
        out.add("  payments now answers over the network: " + remote.networkCalls() + " call");
        out.add("  lines changed in the orders module: 0");

        out.add("");
        out.add("FIVE. The bill: still one program.");
        out.add("  3 modules, 1 build, 1 deployment: a payments fix redeploys the catalogue too");
        out.add("  one process: a crash in any module stops them all, and they scale together");
        out.add("  and the boundaries last only as long as the check runs on every build");
        return out;
    }

    private ModularMonolithDemo() {
    }
}
