package com.jk.explore.featuretoggle;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/** A table of switches, read at run time. The code is deployed once; the table changes. */
public class Toggles {

    private final Map<String, Rule> rules = new HashMap<>();
    private final Map<String, Integer> created = new HashMap<>();
    private boolean reachable = true;

    public void define(String name, Rule rule, int createdDay) {
        rules.put(name, rule);
        created.put(name, createdDay);
    }

    public void set(String name, Rule rule) {
        rules.put(name, rule);
    }

    public void storeDown() {
        reachable = false;
    }

    public void storeUp() {
        reachable = true;
    }

    /** An unknown toggle, or an unreachable table, means off: the safe answer. */
    public boolean isOn(String name, String customerId) {
        if (!reachable) {
            return false;
        }
        Rule rule = rules.get(name);
        if (rule instanceof Rule.On) {
            return true;
        }
        if (rule instanceof Rule.Percent p) {
            return bucket(customerId) < p.percent();
        }
        if (rule instanceof Rule.Only o) {
            return o.customers().contains(customerId);
        }
        return false;
    }

    /** The customer number, taken modulo 100: "c37" is bucket 37. */
    static int bucket(String customerId) {
        return Integer.parseInt(customerId.substring(1)) % 100;
    }

    /** Toggles that are fully on or fully off and older than the limit: nobody is deciding anything with them now. */
    public List<String> stale(int today, int maxAgeDays) {
        List<String> names = new ArrayList<>();
        for (Map.Entry<String, Rule> e : rules.entrySet()) {
            boolean settled = e.getValue() instanceof Rule.On || e.getValue() instanceof Rule.Off;
            if (settled && today - created.get(e.getKey()) > maxAgeDays) {
                names.add(e.getKey());
            }
        }
        names.sort(null);
        return names;
    }

    public int count() {
        return rules.size();
    }
}
