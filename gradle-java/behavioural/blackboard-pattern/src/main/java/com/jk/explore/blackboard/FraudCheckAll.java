package com.jk.explore.blackboard;

import java.util.Map;

/**
 * Without the pattern: one method that runs every check, in a fixed order, every time.
 *
 * <p>The order is written by hand (both country lookups must come before the
 * comparison), every check runs even after the answer is clear, and adding a
 * check means editing this method.
 */
public final class FraudCheckAll {

    private int spentMs;

    public String decide(Map<String, String> order) {
        int risk = 0;
        String cardCountry = Checks.CARD_COUNTRY.getOrDefault(order.get("card"), "??");
        spentMs += 20;
        String ipCountry = Checks.IP_COUNTRY.getOrDefault(order.get("ip"), "??");
        spentMs += 30;
        if (!cardCountry.equals(ipCountry)) {
            risk += 40;
        }
        spentMs += 1;
        if (Integer.parseInt(order.get("ordersLastHour")) > 3) {
            risk += 30;
        }
        spentMs += 50;
        if (Long.parseLong(order.get("totalPence")) > 50000) {
            risk += 20;
        }
        spentMs += 1;
        if (order.get("device").startsWith("emulator")) {
            risk += 25;
        }
        spentMs += 800;
        return risk >= Controller.REJECT_AT ? "REJECT" : "APPROVE";
    }

    public int spentMs() {
        return spentMs;
    }
}
