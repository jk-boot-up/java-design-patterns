package com.jk.explore.flyweight;

import java.util.List;

public class BadgeDemo {

    private static final int CATALOG_SIZE = 100_000;

    public static void main(String[] args) {
        System.out.println("== Rendering badges for five listings ==");
        List<CatalogBadge> sample = List.of(
                new CatalogBadge(BadgeType.NEW, "LST-1001", null),
                new CatalogBadge(BadgeType.SALE, "LST-1002", null),
                new CatalogBadge(BadgeType.SALE, "LST-1003", "Flash Sale"),
                new CatalogBadge(BadgeType.BESTSELLER, "LST-1004", null),
                new CatalogBadge(BadgeType.LOW_STOCK, "LST-1005", "Only 2 left")
        );
        sample.forEach(badge -> System.out.println(badge.render()));

        System.out.println();
        System.out.println("== Proving the sharing ==");
        BadgeStyle first = BadgeStyleFactory.styleFor(BadgeType.SALE);
        BadgeStyle second = BadgeStyleFactory.styleFor(BadgeType.SALE);
        System.out.println("styleFor(SALE) == styleFor(SALE): " + (first == second));
        System.out.println("sample.get(1).style() == sample.get(2).style(): "
                + (sample.get(1).style() == sample.get(2).style()));
        System.out.println("BadgeStyle instances actually created: " + BadgeStyleFactory.instancesCreated());

        System.out.println();
        System.out.println("== The naive alternative, for comparison ==");
        NaiveListingBadge naiveA = new NaiveListingBadge(BadgeType.SALE, "LST-1002");
        NaiveListingBadge naiveB = new NaiveListingBadge(BadgeType.SALE, "LST-1003");
        System.out.println("naiveA == naiveB (both SALE): " + (naiveA == naiveB));

        System.out.println();
        System.out.println("== Memory arithmetic for a " + CATALOG_SIZE + "-listing catalog ==");
        long artworkBytes = first.artworkBytes();
        long naiveTotal = (long) CATALOG_SIZE * artworkBytes;
        long flyweightTotal = (long) BadgeType.values().length * artworkBytes;
        System.out.printf("Naive:      %,d badges x %d KB artwork each = %,d MB%n",
                CATALOG_SIZE, artworkBytes / 1024, naiveTotal / (1024 * 1024));
        System.out.printf("Flyweight:  %d styles x %d KB artwork each     = %,d KB%n",
                BadgeType.values().length, artworkBytes / 1024, flyweightTotal / 1024);
        System.out.printf("Savings:    %,d MB avoided by sharing %d instances instead of %,d%n",
                (naiveTotal - flyweightTotal) / (1024 * 1024), BadgeType.values().length, CATALOG_SIZE);
    }
}
