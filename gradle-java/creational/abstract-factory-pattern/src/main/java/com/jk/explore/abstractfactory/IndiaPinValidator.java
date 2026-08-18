package com.jk.explore.abstractfactory;

import java.util.regex.Pattern;

public class IndiaPinValidator implements AddressValidator {

    private static final Pattern FORMAT = Pattern.compile("^[1-9]\\d{5}$");

    @Override
    public String postcodeLabel() {
        return "PIN code";
    }

    @Override
    public boolean isValid(String postcode) {
        return postcode != null && FORMAT.matcher(postcode.trim()).matches();
    }
}
