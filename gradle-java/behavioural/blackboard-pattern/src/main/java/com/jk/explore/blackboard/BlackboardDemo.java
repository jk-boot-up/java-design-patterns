package com.jk.explore.blackboard;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * The five acts: one method that runs every check, the blackboard, stopping early, a new check, and the bill.
 */
public final class BlackboardDemo {

    public static void main(String[] args) {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    static Map<String, String> goodOrder() {
        return Map.of("card", "4000-GB", "ip", "81.2.69.1", "ordersLastHour", "1", "totalPence", "4000",
                "device", "iphone-12", "items", "kettle");
    }

    static Map<String, String> riskyOrder() {
        return Map.of("card", "4000-GB", "ip", "95.31.18.9", "ordersLastHour", "5", "totalPence", "4000",
                "device", "emulator-x86", "items", "kettle");
    }

    static Map<String, String> giftCardOrder() {
        return Map.of("card", "4000-GB", "ip", "81.2.69.1", "ordersLastHour", "1", "totalPence", "30000",
                "device", "iphone-12", "items", "gift card x6");
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() {
        List<String> out = new ArrayList<>();

        out.add("ONE. One method runs every check, in a fixed order.");
        FraudCheckAll all = new FraudCheckAll();
        out.add("  risky order: " + all.decide(riskyOrder()) + " after all 6 checks, " + all.spentMs() + " ms");
        out.add("  the answer was clear after 5 cheap checks; the 800 ms device check ran anyway");
        out.add("  a new check means editing this method, and getting the order right by hand");

        out.add("");
        out.add("TWO. The blackboard: checks add what they know to a shared board.");
        Blackboard b1 = new Blackboard(goodOrder());
        Controller c1 = new Controller(Checks.standard());
        String d1 = c1.decide(b1);
        b1.log().forEach(line -> out.add("  " + line));
        out.add("  good order: " + d1 + ", risk " + b1.risk() + ", " + c1.ran() + " checks, " + c1.spentMs() + " ms");

        out.add("");
        out.add("THREE. The controller stops as soon as it can decide.");
        Blackboard b2 = new Blackboard(riskyOrder());
        Controller c2 = new Controller(Checks.standard());
        String d2 = c2.decide(b2);
        b2.log().stream().filter(l -> l.contains("risk")).forEach(line -> out.add("  " + line));
        out.add("  risky order: " + d2 + " at risk " + b2.risk() + " after " + c2.ran() + " checks, " + c2.spentMs()
                + " ms; the device check never ran");

        out.add("");
        out.add("FOUR. A new check joins without changing the others.");
        List<KnowledgeSource> withGift = new ArrayList<>(Checks.standard());
        withGift.add(Checks.giftCards());
        Blackboard b3 = new Blackboard(giftCardOrder());
        Controller c3 = new Controller(withGift);
        String d3 = c3.decide(b3);
        out.add("  6 gift cards, £300: " + d3 + ", " + b3.log().get(b3.log().size() - 1).split(": ", 2)[1]);
        out.add("  without the new check it would have been: "
                + new Controller(Checks.standard()).decide(new Blackboard(giftCardOrder())));

        out.add("");
        out.add("FIVE. The bill: nobody wrote down the order of events.");
        out.add("  the checks ran in an order chosen at run time, so the log is the only story");
        out.add("  every check can read every fact on the board, including the card number");
        return out;
    }

    private BlackboardDemo() {
    }
}
