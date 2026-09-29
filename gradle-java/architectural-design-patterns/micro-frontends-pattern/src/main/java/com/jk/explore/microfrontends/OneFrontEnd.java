package com.jk.explore.microfrontends;

/**
 * Without the pattern: one front-end application renders every part of the product page, and fails as one.
 */
public final class OneFrontEnd {

    private boolean recommendationsBroken;

    public String productPage(String sku) {
        StringBuilder page = new StringBuilder();
        page.append("[product] steel kettle, £30.00 | ");
        page.append("[basket] 2 items, £38.00 | ");
        if (recommendationsBroken) {
            throw new IllegalStateException("recommendations: index out of range");
        }
        page.append("[recommendations] mug, teapot");
        return page.toString();
    }

    public void breakRecommendations() {
        recommendationsBroken = true;
    }
}
