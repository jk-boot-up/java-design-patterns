package com.jk.explore.sidecarkubernetes;

/**
 * What a manifest says about one container: a name, an image, and the port it
 * listens on (0 for none). Immutable, because a manifest is text somebody
 * wrote, and injection must not be able to change it.
 */
public record ContainerSpec(String name, String image, int port) {
}
