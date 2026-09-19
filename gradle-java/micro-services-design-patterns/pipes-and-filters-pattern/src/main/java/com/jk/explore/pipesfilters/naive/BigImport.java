package com.jk.explore.pipesfilters.naive;

import java.util.ArrayList;
import java.util.List;

/**
 * Importing orders in one method: parsing, checking, pricing, tax and formatting, all in one loop.
 * It is correct. Nothing in it can be run, tested or changed on its own.
 */
public class BigImport {

    public static List<String> run(List<String> lines) {
        List<String> out = new ArrayList<>();
        for (String line : lines) {
            String[] p = line.split(",");
            if (p.length != 3) {
                continue;
            }
            int q;
            try {
                q = Integer.parseInt(p[2].trim());
            } catch (NumberFormatException e) {
                continue;
            }
            if (q < 1 || q > 10) {
                continue;
            }
            String sku = p[1].trim();
            long net = (sku.startsWith("ESP") ? 30000L : 800L) * q;
            long gross = net + net / 5;
            out.add(String.format("%s: %d x %s = £%d.%02d", p[0].trim(), q, sku, gross / 100, gross % 100));
        }
        return out;
    }

    /** The separate jobs done inside the one method. */
    public static int jobsInOneMethod() {
        return 5;
    }
}
