package com.jk.explore.priorityqueue;

/**
 * An order waiting to be picked: same-day orders must reach the courier's van by the cut-off.
 */
public record Order(String id, boolean sameDay, int arrivedMinute, long seq) {
}
