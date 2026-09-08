package com.jk.explore.decorator;

import java.math.BigDecimal;

public interface PricedItem {
    BigDecimal cost();

    String description();
}
