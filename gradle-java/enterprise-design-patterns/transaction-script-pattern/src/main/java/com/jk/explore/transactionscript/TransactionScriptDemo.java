package com.jk.explore.transactionscript;

import com.jk.explore.transactionscript.script.*;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

public class TransactionScriptDemo {

    public static void main(String[] args) throws IOException {
        one();
        two();
        three();
        four();
        five();
        six();
    }

    private static String pounds(long pence) {
        return String.format("£%d.%02d", pence / 100, pence % 100);
    }

    private static void one() {
        System.out.println("ONE. One request, one procedure.");
        Db db = new Db();
        Db.SavedOrder o = new PlaceOrderScript(db, new Payment()).run("ada", "MUG-BLUE", 2);
        System.out.println("  " + o.id() + " for " + pounds(o.totalPence()) + ". stock of MUG-BLUE: " + db.stockOf("MUG-BLUE") + ".");
        System.out.println("  the whole business action is one method, read from the top to the bottom.");
    }

    private static void two() {
        System.out.println("TWO. One transaction.");
        Db db = new Db();
        Payment payment = new Payment();
        payment.declineNext();
        try {
            new PlaceOrderScript(db, payment).run("ada", "MUG-BLUE", 2);
        } catch (IllegalStateException e) {
            System.out.println("  " + e.getMessage() + " after the stock was taken.");
        }
        System.out.println("  stock of MUG-BLUE: " + db.stockOf("MUG-BLUE") + ". orders saved: " + db.orders().size() + ". the script's changes were undone together.");
    }

    private static void three() {
        System.out.println("THREE. A second script copies the rule.");
        Db db = new Db();
        Db.SavedOrder o = new PlaceOrderScript(db, new Payment()).run("ada", "MUG-BLUE", 7);
        long amended = new AmendOrderScript(db).run(o.id(), "MUG-BLUE", 7);
        System.out.println("  7 mugs placed: " + pounds(o.totalPence()) + ". the same 7 mugs amended: " + pounds(amended) + ".");
        System.out.println("  the bulk discount changed from 10 items to 5. one script was told, the other was not.");
    }

    private static void four() {
        System.out.println("FOUR. Share a procedure.");
        System.out.println("  7 mugs priced by the shared helper: " + pounds(Pricing.total("MUG-BLUE", 7)) + " in both scripts.");
        System.out.println("  it is still procedural. there is no Order object, only a function both scripts call.");
    }

    private static void five() throws IOException {
        System.out.println("FIVE. The bill: growth.");
        int before = branches("PlaceOrderScript.java");
        int after = branches("PlaceOrderScriptGrown.java");
        System.out.println("  decisions in the first script: " + before + ", so " + (1 << before) + " paths to test.");
        System.out.println("  decisions after three more rules: " + after + ", so " + (1 << after) + " paths to test.");
        System.out.println("  every new rule went in the middle of one method.");
    }

    private static void six() {
        System.out.println("SIX. Where a script is right.");
        Db db = new Db();
        PlaceOrderScript place = new PlaceOrderScript(db, new Payment());
        place.run("ada", "MUG-BLUE", 2);
        place.run("ben", "ESP-001", 1);
        System.out.println("  month end: " + MonthEndScript.run(db) + ".");
        System.out.println("  a job with one purpose and a few rules is clearer as a script than as a set of objects.");
    }

    /** Counts the decisions in a script's source: every if. */
    static int branches(String file) throws IOException {
        String text = Files.readString(Path.of("src/main/java/com/jk/explore/transactionscript/script/" + file));
        int n = 0;
        for (String line : text.split("\n")) {
            if (line.trim().startsWith("if (")) {
                n++;
            }
        }
        return n;
    }
}
