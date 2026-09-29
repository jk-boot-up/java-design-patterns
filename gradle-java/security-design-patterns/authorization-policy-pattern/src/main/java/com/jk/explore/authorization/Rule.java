package com.jk.explore.authorization;

import java.util.function.Predicate;

/**
 * One line of the policy: this action is allowed when this condition holds.
 */
public record Rule(String action, String description, Predicate<Request> condition) {
}
