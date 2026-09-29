package com.jk.explore.cellbased;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.IntStream;

/**
 * The five acts: one shared stack, cells behind a router, a bad release in one cell, a new cell, and the bill.
 */
public final class CellBasedDemo {

    static final List<String> CUSTOMERS = IntStream.rangeClosed(1, 30).mapToObj(i -> "C-" + i).toList();

    public static void main(String[] args) {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    static int failures(CellRouter router, List<String> customers) {
        int failed = 0;
        for (String c : customers) {
            try {
                router.checkout(c, 2000);
            } catch (IllegalStateException e) {
                failed++;
            }
        }
        return failed;
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() {
        List<String> out = new ArrayList<>();

        out.add("ONE. One shared stack for every customer.");
        Cell everything = new Cell("the whole shop");
        CellRouter one = new CellRouter();
        one.addCell(everything);
        one.place(CUSTOMERS);
        everything.deploy("v2-buggy");
        out.add("  a release with a checkout bug goes out");
        out.add("  customers who could not check out: " + failures(one, CUSTOMERS) + " of " + CUSTOMERS.size());

        out.add("");
        out.add("TWO. Cells: three complete copies of the shop, customers split between them.");
        CellRouter router = new CellRouter();
        for (String name : new String[] {"cell-1", "cell-2", "cell-3"}) {
            router.addCell(new Cell(name));
        }
        router.place(CUSTOMERS);
        Map<String, Long> perCell = new LinkedHashMap<>();
        for (String c : CUSTOMERS) {
            perCell.merge(router.cellOf(c).name(), 1L, Long::sum);
        }
        out.add("  customers per cell: " + perCell);
        out.add("  C-1 -> " + router.checkout("C-1", 2000) + "; C-2 -> " + router.checkout("C-2", 2000));
        out.add("  failures: " + failures(router, CUSTOMERS));

        out.add("");
        out.add("THREE. A bad release reaches one cell, not everyone.");
        router.cells().get(0).deploy("v2-buggy");
        out.add("  the buggy release goes to cell-1 first");
        out.add("  customers who could not check out: " + failures(router, CUSTOMERS) + " of " + CUSTOMERS.size());
        router.cells().get(0).deploy("v1");
        out.add("  cell-1 rolled back: failures " + failures(router, CUSTOMERS) + "; cells 2 and 3 never noticed");

        out.add("");
        out.add("FOUR. More customers? Add a cell.");
        Cell cell4 = new Cell("cell-4");
        router.addCell(cell4);
        router.sendNewCustomersTo(cell4);
        List<String> newcomers = IntStream.rangeClosed(31, 36).mapToObj(i -> "C-" + i).toList();
        for (String c : newcomers) {
            router.checkout(c, 2000);
        }
        out.add("  6 new customers placed in " + router.cellOf("C-31").name() + "; C-1 still in " + router.cellOf("C-1").name());
        out.add("  no existing customer was moved");

        out.add("");
        out.add("FIVE. The bill: every cell is a separate world.");
        long total = router.cells().stream().mapToLong(Cell::salesPence).sum();
        out.add("  \"today's total sales\" means asking all " + router.cells().size() + " cells: " + pounds(total));
        out.add("  and 4 copies of every service and database to run, watch and pay for");
        return out;
    }

    static String pounds(long pence) {
        return String.format("£%d.%02d", pence / 100, pence % 100);
    }

    private CellBasedDemo() {
    }
}
