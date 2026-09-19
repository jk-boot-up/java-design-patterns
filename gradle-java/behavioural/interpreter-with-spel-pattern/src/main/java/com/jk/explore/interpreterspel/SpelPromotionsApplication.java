package com.jk.explore.interpreterspel;

import org.springframework.expression.ExpressionException;

public class SpelPromotionsApplication {

    static final String[] PROMOTIONS = {
            "WELCOME10 | 10 | firstOrder",
            "UKBIG | 15 | country == 'UK' and basketPence > 5000",
            "BULK | 20 | items >= 5 or basketPence > 20000",
            "NOTUK | 5 | !(country == 'UK')"
    };

    static final Order ASHA = new Order("UK", 6_000, 2, false, null);
    static final Order BEN = new Order("DE", 3_000, 1, true, "SPRING");
    static final Order CAROL = new Order("UK", 25_000, 6, false, null);

    public static void main(String[] args) {
        System.out.println("ONE. The rules are text.");
        PromotionBook book = new PromotionBook(false, PROMOTIONS);
        for (String line : PROMOTIONS) {
            System.out.println("  " + line);
        }
        System.out.println("  asha  (UK, 60.00, 2 items):            " + book.applicableTo(ASHA));
        System.out.println("  ben   (DE, 30.00, 1 item, first):      " + book.applicableTo(BEN));
        System.out.println("  carol (UK, 250.00, 6 items):           " + book.applicableTo(CAROL));

        System.out.println("TWO. The language came free.");
        PromotionBook extras = new PromotionBook(false,
                "SMALLUK | 5 | country == 'UK' ? basketPence < 5000 : false",
                "VOUCHER | 8 | voucher != null and voucher matches 'SPR.*'",
                "MODULO | 1 | items % 2 == 0");
        System.out.println("  a conditional, a pattern match and a remainder, and nothing new was written:");
        System.out.println("  ben:   " + extras.applicableTo(BEN));
        System.out.println("  asha:  " + extras.applicableTo(ASHA));

        System.out.println("THREE. A typo in the language, and a typo in a name.");
        try {
            new PromotionBook(false, "OOPS | 5 | country == 'UK' and and basketPence > 5000");
        } catch (ExpressionException e) {
            System.out.println("  a rule that is not a valid expression is refused when the book is built: " + e.getClass().getSimpleName() + ".");
        }
        PromotionBook typo = new PromotionBook(false, "OOPS | 5 | contry == 'UK'");
        System.out.println("  a misspelled property is accepted when the book is built.");
        try {
            typo.applicableTo(ASHA);
        } catch (ExpressionException e) {
            System.out.println("  it fails when the first order arrives: " + e.getClass().getSimpleName() + ".");
        }

        System.out.println("FOUR. The language can reach the whole program.");
        String hostile = "T(java.lang.System).getProperty('java.specification.version') != null";
        PromotionBook trusting = new PromotionBook(true, "HOSTILE | 99 | " + hostile);
        System.out.println("  with the full context, a rule can call any static method: " + trusting.applicableTo(ASHA) + ".");
        PromotionBook readOnly = new PromotionBook(false, "HOSTILE | 99 | " + hostile);
        try {
            readOnly.applicableTo(ASHA);
        } catch (ExpressionException e) {
            System.out.println("  with the read-only context it is refused: " + e.getClass().getSimpleName() + ".");
        }
        try {
            new PromotionBook(false, "LONG | 8 | voucher != null and voucher.length() > 3").applicableTo(BEN);
        } catch (ExpressionException e) {
            System.out.println("  it also refuses a method call, voucher.length(): " + e.getClass().getSimpleName() + ". a rule can only read properties.");
        }
        System.out.println("  rules written by marketing are input. Use the read-only context.");

        System.out.println("FIVE. Missing values.");
        PromotionBook unsafe = new PromotionBook(false, "LONGVOUCHER | 8 | voucher.empty == false");
        try {
            unsafe.applicableTo(ASHA);
        } catch (ExpressionException e) {
            System.out.println("  asha has no voucher, and voucher.empty fails: " + e.getClass().getSimpleName() + ".");
        }
        PromotionBook safe = new PromotionBook(false, "LONGVOUCHER | 8 | voucher?.empty == false");
        System.out.println("  with the safe-navigation operator, asha: " + safe.applicableTo(ASHA) + ", ben: " + safe.applicableTo(BEN) + ".");

        System.out.println("SIX. Parsed once, used many times.");
        PromotionBook many = new PromotionBook(false, PROMOTIONS);
        int matches = 0;
        for (int i = 0; i < 1000; i++) {
            matches += many.applicableTo(i % 2 == 0 ? ASHA : CAROL).size();
        }
        System.out.println("  1000 orders through the same four parsed rules: " + matches + " promotions applied.");
        System.out.println("  the tree was built four times, at startup, not four thousand.");
    }
}
