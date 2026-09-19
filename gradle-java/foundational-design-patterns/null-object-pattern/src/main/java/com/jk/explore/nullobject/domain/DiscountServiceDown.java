package com.jk.explore.nullobject.domain;

/** The discount service could not be reached. That is not the same as "no discount". */
public class DiscountServiceDown extends RuntimeException {

    public DiscountServiceDown() {
        super("the discount service is down");
    }
}
