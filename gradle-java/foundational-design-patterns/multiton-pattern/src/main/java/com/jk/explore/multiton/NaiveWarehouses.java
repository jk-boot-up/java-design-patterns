package com.jk.explore.multiton;

import java.util.HashMap;
import java.util.Map;

/** Looks first and creates second, with no lock between the two. */
public class NaiveWarehouses {

    private final Map<String, Warehouse> instances = new HashMap<>();
    private final Runnable betweenLookAndCreate;

    public NaiveWarehouses(Runnable betweenLookAndCreate) {
        this.betweenLookAndCreate = betweenLookAndCreate;
    }

    public Warehouse of(String region) {
        Warehouse found;
        synchronized (instances) {
            found = instances.get(region);
        }
        if (found == null) {
            betweenLookAndCreate.run();
            Warehouse made = Warehouse.unshared(region);
            synchronized (instances) {
                instances.put(region, made);
            }
            return made;
        }
        return found;
    }
}
