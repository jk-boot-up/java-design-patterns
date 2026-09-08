package com.jk.explore.visitor;

import java.util.ArrayList;
import java.util.List;

/**
 * Report three: the catalog as a CSV file, for the finance spreadsheet.
 *
 * <p>Look at what is in this class: a header row, a quoting rule, and a
 * decision about how to render a bundle. All three are facts about CSV, and
 * none of them is a fact about a product. In the naive design they live in
 * {@link NaiveProduct} and {@link NaiveBundle} — a domain class knowing that
 * a comma inside a field means the field needs double quotes, and knowing
 * it twice.
 *
 * <p>Knowing it twice is how it ends up known differently. See
 * {@link NaiveBundle#appendCsvTo}.
 */
public final class CsvExportVisitor extends CategoryPathVisitor {

    public static final String HEADER =
            "category,sku,name,type,unit_price,stock,restriction";

    private final List<String> rows = new ArrayList<>();

    @Override
    public void visit(Product product) {
        rows.add(row(path(), product.sku(), product.name(), "product",
                product.price(), product.stockOnHand(),
                product.restriction().label()));
    }

    @Override
    public void visit(Bundle bundle) {
        // A bundle exports as one row at its kit price. Its contents are
        // not rows: they are already on the file under their own SKUs, and
        // finance would be adding the same stock in twice.
        rows.add(row(path(), bundle.sku(), bundle.name(), "bundle",
                bundle.price(), bundle.stockOnHand(), ""));
    }

    private String row(String category, String sku, String name, String type,
                       Money price, int stock, String restriction) {
        return String.join(",",
                quote(category), quote(sku), quote(name), type,
                String.format("%.2f", price.asPence() / 100.0),
                String.valueOf(stock), quote(restriction));
    }

    /**
     * RFC 4180: a field containing a comma, a quote or a newline is wrapped
     * in double quotes, and any quote inside it is doubled. The catalog
     * contains at least one product name with a comma in it, so this rule is
     * load-bearing rather than defensive.
     */
    static String quote(String field) {
        if (field.indexOf(',') < 0 && field.indexOf('"') < 0
                && field.indexOf('\n') < 0) {
            return field;
        }
        return '"' + field.replace("\"", "\"\"") + '"';
    }

    /** The data rows, without the header, in tree order. */
    public List<String> rows() {
        return List.copyOf(rows);
    }

    /** The finished file, header included. */
    public String csv() {
        StringBuilder out = new StringBuilder(HEADER);
        for (String row : rows) {
            out.append('\n').append(row);
        }
        return out.toString();
    }
}
