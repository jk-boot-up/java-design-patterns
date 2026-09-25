package com.jk.explore.springcloudconfig.shop;

import java.math.BigDecimal;
import java.math.RoundingMode;

/** Formats an amount of money the way the shop prints it: £48.00. */
public final class Money {

    private Money() {
    }

    public static String pounds(BigDecimal amount) {
        return "£" + amount.setScale(2, RoundingMode.HALF_UP).toPlainString();
    }
}
