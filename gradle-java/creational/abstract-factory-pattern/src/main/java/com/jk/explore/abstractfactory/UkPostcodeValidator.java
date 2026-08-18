package com.jk.explore.abstractfactory;

import java.util.regex.Pattern;

public class UkPostcodeValidator implements AddressValidator {

    private static final Pattern FORMAT =
            Pattern.compile("^[A-Z]{1,2}\\d[A-Z\\d]? ?\\d[A-Z]{2}$");

    @Override
    public String postcodeLabel() {
        return "postcode";
    }

    @Override
    public boolean isValid(String postcode) {
        return postcode != null && FORMAT.matcher(postcode.trim().toUpperCase()).matches();
    }
}
