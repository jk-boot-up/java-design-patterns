package com.jk.explore.decorator;

import java.util.Objects;

public abstract class ProductDecorator implements PricedItem {

    protected final PricedItem wrapped;

    protected ProductDecorator(PricedItem wrapped) {
        this.wrapped = Objects.requireNonNull(wrapped);
    }
}
