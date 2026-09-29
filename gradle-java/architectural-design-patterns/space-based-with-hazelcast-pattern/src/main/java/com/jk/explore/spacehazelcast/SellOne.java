package com.jk.explore.spacehazelcast;

import com.hazelcast.map.EntryProcessor;
import java.util.Map;

/**
 * Sells one item, run by Hazelcast on the member that owns the key, one at a time for that key:
 * two units cannot both sell the last kettle.
 */
public final class SellOne implements EntryProcessor<String, Integer, Boolean> {

    @Override
    public Boolean process(Map.Entry<String, Integer> entry) {
        int stock = entry.getValue() == null ? 0 : entry.getValue();
        if (stock <= 0) {
            return false;
        }
        entry.setValue(stock - 1);
        return true;
    }
}
