package com.jk.explore.contractstub;

import java.util.Map;

/**
 * One agreed exchange: for this request, the provider replies with this.
 */
public record Interaction(String description, Map<String, String> request, Map<String, String> reply) {
}
