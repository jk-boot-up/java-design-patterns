package com.jk.explore.authorization;

/**
 * A signed-in user and their role: CUSTOMER, SUPPORT or ADMIN.
 */
public record User(String name, String role) {
}
