package com.jk.explore.contentrouter;

/** An order message. What it contains decides where it goes. */
public record Order(String id, String kind, String region, long pence) {
}
