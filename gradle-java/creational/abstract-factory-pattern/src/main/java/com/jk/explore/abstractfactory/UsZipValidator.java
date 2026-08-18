package com.jk.explore.abstractfactory;

import java.util.regex.Pattern;

public class UsZipValidator implements AddressValidator {

    private static final Pattern FORMAT = Pattern.compile("^\\d{5}(-\\d{4})?$");

    @Override
    public String postcodeLabel() {
        return "ZIP code";
    }

    @Override
    public boolean isValid(String postcode) {
        return postcode != null && FORMAT.matcher(postcode.trim()).matches();
    }
}
