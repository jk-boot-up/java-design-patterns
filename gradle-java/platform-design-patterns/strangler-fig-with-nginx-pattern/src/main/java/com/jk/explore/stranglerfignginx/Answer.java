package com.jk.explore.stranglerfignginx;

/**
 * What the customer's browser got back: the status code, which service answered, and the text.
 *
 * <p>Both shop services put their own name in a response header called {@code X-Served-By}.
 * NGINX passes that header through untouched, so the customer's side can always tell which
 * service really answered. When NGINX answers by itself, as it does with a 502, the header is
 * missing and {@code servedBy} says {@code nginx}.
 */
public record Answer(int status, String servedBy, String body) {

    public boolean fromOldShop() {
        return OldShop.NAME.equals(servedBy);
    }

    public boolean fromNewService() {
        return NewService.NAME.equals(servedBy);
    }
}
