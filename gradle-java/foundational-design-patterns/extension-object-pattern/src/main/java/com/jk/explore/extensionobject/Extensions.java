package com.jk.explore.extensionobject;

/**
 * The extra roles a product can take on. Each is owned by a different part of the shop.
 */
public final class Extensions {

    /** Owned by the downloads team: e-books and software. */
    public record Download(String url, int maxDownloads) {
    }

    /** Owned by the after-sales team: electricals. */
    public record Warranty(int years) {
    }

    /** Added in act four by the subscriptions team, without editing Product. */
    public record Subscription(int everyWeeks) {
    }

    private Extensions() {
    }
}
