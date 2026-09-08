package com.jk.explore.singleton;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.lang.reflect.Constructor;

public final class OrderSequenceGeneratorDemo {

    public static void main(String[] args) throws Exception {
        System.out.println("== The fix: an enum singleton ==");
        OrderSequenceGenerator first = OrderSequenceGenerator.INSTANCE;
        OrderSequenceGenerator second = OrderSequenceGenerator.INSTANCE;
        System.out.println("first == second: " + (first == second));
        System.out.println(first.nextOrderNumber());
        System.out.println(first.nextOrderNumber());
        System.out.println(second.nextOrderNumber() + "  (issued from 'second', same counter)");

        System.out.println();
        System.out.println("== Attacking it: reflection ==");
        try {
            Constructor<OrderSequenceGenerator> ctor =
                    OrderSequenceGenerator.class.getDeclaredConstructor(String.class, int.class);
            ctor.setAccessible(true);
            ctor.newInstance("FORGED", 99);
            System.out.println("Reflection built a second instance (this should not print)");
        } catch (IllegalArgumentException e) {
            System.out.println("Rejected: " + e.getMessage());
        }

        System.out.println();
        System.out.println("== Attacking it: serialization ==");
        OrderSequenceGenerator roundTripped = roundTripThroughSerialization(first);
        System.out.println("roundTripped == INSTANCE: " + (roundTripped == OrderSequenceGenerator.INSTANCE));

        System.out.println();
        System.out.println("== The trap: a classic private-constructor singleton ==");
        LegacyOrderSequenceGenerator legacyFirst = LegacyOrderSequenceGenerator.getInstance();
        LegacyOrderSequenceGenerator legacySecond = LegacyOrderSequenceGenerator.getInstance();
        System.out.println("legacyFirst == legacySecond: " + (legacyFirst == legacySecond));
        System.out.println(legacyFirst.nextOrderNumber());
        System.out.println(legacyFirst.nextOrderNumber());

        System.out.println();
        System.out.println("== Breaking it: reflection ==");
        Constructor<LegacyOrderSequenceGenerator> legacyCtor =
                LegacyOrderSequenceGenerator.class.getDeclaredConstructor();
        legacyCtor.setAccessible(true);
        LegacyOrderSequenceGenerator forged = legacyCtor.newInstance();
        System.out.println("forged == legacyFirst: " + (forged == legacyFirst));
        System.out.println("forged's first order number: " + forged.nextOrderNumber()
                + "  (a duplicate of one already issued above)");

        System.out.println();
        System.out.println("== Breaking it: serialization ==");
        LegacyOrderSequenceGenerator legacyRoundTripped = roundTripThroughSerialization(legacyFirst);
        System.out.println("legacyRoundTripped == legacyFirst: " + (legacyRoundTripped == legacyFirst));
    }

    private static <T> T roundTripThroughSerialization(T value) throws Exception {
        ByteArrayOutputStream bytes = new ByteArrayOutputStream();
        try (ObjectOutputStream out = new ObjectOutputStream(bytes)) {
            out.writeObject(value);
        }
        try (ObjectInputStream in = new ObjectInputStream(new ByteArrayInputStream(bytes.toByteArray()))) {
            @SuppressWarnings("unchecked")
            T result = (T) in.readObject();
            return result;
        }
    }
}
