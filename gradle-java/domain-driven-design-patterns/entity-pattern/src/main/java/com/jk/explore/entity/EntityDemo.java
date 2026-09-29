package com.jk.explore.entity;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * The five acts: a customer defined by values, a customer with an identity, two people who look alike, a life story, and the bill.
 */
public final class EntityDemo {

    public static void main(String[] args) {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() {
        List<String> out = new ArrayList<>();

        out.add("ONE. A customer defined by its values.");
        CustomerRecord before = new CustomerRecord("Priya", "priya@old.example", 120);
        Map<CustomerRecord, String> ordersByCustomer = new HashMap<>();
        ordersByCustomer.put(before, "ORD-1, ORD-2");
        CustomerRecord after = new CustomerRecord("Priya", "priya@new.example", 120);
        out.add("  Priya changes her email; the old record and the new are equal: " + before.equals(after));
        out.add("  her orders, looked up by the new record: " + ordersByCustomer.get(after));
        Set<CustomerRecord> mailingList = new HashSet<>(List.of(before, after));
        out.add("  customers on the mailing list: " + mailingList.size() + ", both of them Priya");

        out.add("");
        out.add("TWO. An entity: a customer defined by its identity.");
        Customer priya = new Customer(new CustomerId("C-17"), "Priya", "priya@old.example");
        Map<Customer, String> orders = new HashMap<>();
        orders.put(priya, "ORD-1, ORD-2");
        priya.changeEmail("priya@new.example");
        out.add("  " + priya + "; still C-17");
        out.add("  her orders: " + orders.get(priya));
        out.add("  customers on the mailing list: " + new HashSet<>(List.of(priya, priya)).size());

        out.add("");
        out.add("THREE. Two people who look the same are still two people.");
        CustomerRecord tomA = new CustomerRecord("Tom Reed", "reeds@home.example", 0);
        CustomerRecord tomB = new CustomerRecord("Tom Reed", "reeds@home.example", 0);
        out.add("  father and son share a name and a family email; as records, equal: " + tomA.equals(tomB));
        Customer father = new Customer(new CustomerId("C-42"), "Tom Reed", "reeds@home.example");
        Customer son = new Customer(new CustomerId("C-43"), "Tom Reed", "reeds@home.example");
        out.add("  as entities, C-42 and C-43, equal: " + father.equals(son));

        out.add("");
        out.add("FOUR. An entity has a life story.");
        priya.changeEmail("priya@work.example");
        priya.earn(80);
        priya.history().forEach(h -> out.add("  " + h));
        out.add("  three emails, one customer, " + priya.points() + " points; the ID never changed");

        out.add("");
        out.add("FIVE. The bill: equal is not the same as up to date.");
        Customer cached = priya.copy();
        priya.changeEmail("priya@final.example");
        out.add("  a cached copy and the live customer are equal: " + cached.equals(priya));
        out.add("  but the copy says " + cached.email() + " and the live one " + priya.email());
        out.add("  and every entity needs an ID that is unique and never reused");
        return out;
    }

    private EntityDemo() {
    }
}
