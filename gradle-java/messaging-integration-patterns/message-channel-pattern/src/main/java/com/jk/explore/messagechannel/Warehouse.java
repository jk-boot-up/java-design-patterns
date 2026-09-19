package com.jk.explore.messagechannel;

import java.util.ArrayList;
import java.util.List;

/** The warehouse system. It can be taken down, and it records the orders it has been told about. */
public class Warehouse {

    private boolean up = true;
    private final List<String> told = new ArrayList<>();

    public void goDown() {
        up = false;
    }

    public void comeBack() {
        up = true;
    }

    public void pick(String orderId) {
        if (!up) {
            throw new IllegalStateException("the warehouse system is down");
        }
        told.add(orderId);
    }

    public List<String> told() {
        return told;
    }
}
