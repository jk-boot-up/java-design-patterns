package com.jk.explore.writethrough;

import java.util.HashMap;
import java.util.Map;

/**
 * The prices table: the source of truth. 20 ms a write, 10 ms a read, and it can refuse writes.
 */
public final class Database {

    private final Map<String, Long> prices = new HashMap<>();
    private int reads;
    private int writes;
    private long waitedMs;
    private boolean readOnly;

    public Database() {
        prices.put("KETTLE-1", 3000L);
        prices.put("MUG-1", 800L);
    }

    public long read(String sku) {
        reads++;
        waitedMs += 10;
        return prices.get(sku);
    }

    public void write(String sku, long pence) {
        if (readOnly) {
            throw new IllegalStateException("database is read-only for maintenance");
        }
        writes++;
        waitedMs += 20;
        prices.put(sku, pence);
    }

    public void setReadOnly(boolean readOnly) {
        this.readOnly = readOnly;
    }

    public int reads() {
        return reads;
    }

    public int writes() {
        return writes;
    }

    public long waitedMs() {
        return waitedMs;
    }
}
