package com.jk.explore.databaseperservice;

import java.util.LinkedHashMap;
import java.util.Map;

/**
 * The Catalog service's own database. Nobody else may read it.
 *
 * The interesting method is {@link #renameProductNameColumnTo}. In the shared schema
 * that rename broke somebody else's order history page. Here it breaks nothing at
 * all, because the only code that names this column lives in the same repository as
 * the column, is tested alongside it, and is changed in the same commit.
 *
 * <p>That freedom is what a shop is buying when it splits its database. It is worth
 * remembering that it is not a technical benefit — the query engine was perfectly
 * happy before. It is an organisational one: a team can now change its mind without
 * asking permission.
 */
public final class CatalogDatabase {

    private static final String OWNER = "Catalog";

    /** sku -> (column name -> value). */
    private final Map<String, Map<String, String>> products = new LinkedHashMap<>();
    private final CallLog log;
    private String nameColumn = "product_name";
    private int queries;

    public CatalogDatabase(CallLog log) {
        this.log = log;
    }

    public void insert(String sku, String name) {
        products.put(sku, new LinkedHashMap<>(Map.of(nameColumn, name)));
    }

    /** Removes a product from the catalogue entirely. */
    public void delete(String sku) {
        products.remove(sku);
        log.note("CatalogDb", "DELETED", sku + " removed from the catalogue");
    }

    /**
     * The catalog team's Tuesday-afternoon rename, done safely this time.
     *
     * Note that this method updates {@code nameColumn} as well as the rows, so its own
     * queries follow the change. Nothing outside this class ever named the column.
     */
    public void renameProductNameColumnTo(String newName) {
        for (Map<String, String> row : products.values()) {
            String value = row.remove(nameColumn);
            if (value != null) {
                row.put(newName, value);
            }
        }
        log.note("CatalogDb", "MIGRATED", nameColumn + " -> " + newName);
        nameColumn = newName;
    }

    /**
     * The name of one product, or {@code null} if there is no such product.
     *
     * @throws NotYourDataException if anybody but Catalog asks
     */
    public String nameOf(String requester, String sku) {
        if (!OWNER.equals(requester)) {
            log.note("CatalogDb", "REFUSED", requester + " tried to read Catalog's tables");
            throw new NotYourDataException(requester, OWNER);
        }
        queries++;
        Map<String, String> row = products.get(sku);
        return row == null ? null : row.get(nameColumn);
    }

    public int queries() {
        return queries;
    }
}
