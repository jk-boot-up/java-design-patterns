package com.jk.explore.roleobject;

import java.util.ArrayList;
import java.util.List;

/**
 * The five acts: a subclass per kind of customer, roles on one account, roles with behaviour, dropping a role, and the bill.
 */
public final class RoleObjectDemo {

    public static void main(String[] args) {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() {
        List<String> out = new ArrayList<>();

        out.add("ONE. A subclass for every kind of customer.");
        Subclasses.Customer priya = new Subclasses.Customer("Priya");
        for (int i = 1; i <= 12; i++) {
            priya.placeOrder("ORD-" + i);
        }
        Subclasses.SellingCustomer priyaSeller = new Subclasses.SellingCustomer("Priya", "Priya's Pottery");
        out.add("  Priya has 12 orders, then opens a shop: a new SellingCustomer object");
        out.add("  orders on the new object: " + priyaSeller.orders().size() + "; same person: " + (priya == priyaSeller));
        out.add("  buyer, seller, affiliate in any mix: " + Subclasses.classesNeeded(3) + " classes");

        out.add("");
        out.add("TWO. One account, with roles added as life changes.");
        Account account = new Account("C-17", "Priya");
        Roles.Buyer buyer = account.addRole(new Roles.Buyer(account));
        for (int i = 1; i <= 12; i++) {
            buyer.placeOrder("ORD-" + i);
        }
        account.addRole(new Roles.Seller(account, "Priya's Pottery"));
        out.add("  " + account.name() + " (" + account.id() + ") plays " + account.roleNames());
        out.add("  orders still on the account: " + account.as(Roles.Buyer.class).orElseThrow().orders().size());

        out.add("");
        out.add("THREE. Each role brings its own data and behaviour.");
        out.add("  " + account.as(Roles.Seller.class).orElseThrow().list("hand-thrown mug"));
        Roles.Affiliate affiliate = account.addRole(new Roles.Affiliate(account, 5));
        affiliate.referred(4000);
        affiliate.referred(6000);
        out.add("  she joins the affiliate scheme at 5% and refers £40 and £60 orders: earned "
                + pounds(affiliate.earnedPence()));
        out.add("  Account knows nothing about shops or commission; roles now " + account.roleNames());

        out.add("");
        out.add("FOUR. A role can be dropped while the account lives on.");
        account.removeRole(Roles.Seller.class);
        out.add("  selling suspended; roles now " + account.roleNames());
        out.add("  list another mug: " + account.as(Roles.Seller.class).map(s -> s.list("mug"))
                .orElse("refused, " + account.name() + " is not a seller"));
        account.as(Roles.Buyer.class).orElseThrow().placeOrder("ORD-13");
        out.add("  she can still buy: " + account.as(Roles.Buyer.class).orElseThrow().orders().size() + " orders");

        out.add("");
        out.add("FIVE. The bill: every caller must ask first.");
        out.add("  every use of a role starts with as(...) and a plan for \"no\"");
        out.add("  and her data is spread out: name on the account, shop name on a role that is now gone");
        return out;
    }

    static String pounds(long pence) {
        return String.format("£%d.%02d", pence / 100, pence % 100);
    }

    private RoleObjectDemo() {
    }
}
