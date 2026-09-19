package com.jk.explore.leaderelection;

/** The right to lead until {@code expiresAt}, and a token that goes up every time leadership changes hands. */
public record Lease(String holder, long token, long expiresAt) {
}
