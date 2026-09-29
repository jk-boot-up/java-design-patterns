package com.jk.explore.inputvalidation;

import java.util.ArrayList;
import java.util.List;

/**
 * The five acts: trusting the form, checking at the boundary, parsing into safe types,
 * encoding on the way out, and the bill.
 */
public final class InputValidationDemo {

    static final double MUG_PRICE = 9.99;

    public static void main(String[] args) {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() {
        List<String> out = new ArrayList<>();
        OrderForm bad = new OrderForm("MUG-1", "-5", "not-an-email", "Ana");

        out.add("ONE. The form's text is used as it arrives.");
        out.add("  quantity \"-5\" of a 9.99 mug: total " + String.format("%.2f", NaiveCheckout.total(bad, MUG_PRICE)));
        out.add("  a negative total: the shop would pay the customer");
        out.add("  and \"not-an-email\" is saved as the email address");

        out.add("");
        out.add("TWO. Check every field at the boundary, and report every problem.");
        OrderParser.Result result = OrderParser.parse(new OrderForm("mug 1", "-5", "not-an-email", "Ana"));
        out.add("  " + result.problems().size() + " problems:");
        for (String problem : result.problems()) {
            out.add("    - " + problem);
        }
        OrderParser.Result good = OrderParser.parse(new OrderForm("MUG-1", "2", "ana@example.com", "Ana"));
        out.add("  a good form: accepted, total " + String.format("%.2f", good.order().total(MUG_PRICE)));

        out.add("");
        out.add("THREE. Parse into types that cannot hold bad values.");
        try {
            new Quantity(-5);
        } catch (IllegalArgumentException e) {
            out.add("  new Quantity(-5): " + e.getMessage());
        }
        out.add("  checkout takes a ValidOrder, so it never has to check again");

        out.add("");
        out.add("FOUR. Valid is not the same as safe everywhere: encode on the way out.");
        String review = "Lovely mug <script>steal(document.cookie)</script>";
        out.add("  a review, shown as it is: " + review);
        out.add("  shown encoded:            " + Html.escape(review));
        out.add("  the page now shows the text instead of running it");

        out.add("");
        out.add("FIVE. The bill: rules that are fair, and checked on the server.");
        String name = "Siobhán O'Brien";
        out.add("  \"" + name + "\" with the rule [A-Za-z ]: "
                + (CustomerName.TOO_STRICT.matcher(name).matches() ? "accepted" : "REJECTED, a real customer turned away"));
        out.add("  with a rule for letters in any alphabet: "
                + (CustomerName.FAIR.matcher(name).matches() ? "accepted" : "rejected"));
        out.add("  checks in the browser are a convenience; a request sent without the browser skips them");
        return out;
    }

    private InputValidationDemo() {
    }
}
