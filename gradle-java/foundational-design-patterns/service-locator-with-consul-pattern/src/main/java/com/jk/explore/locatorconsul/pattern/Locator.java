package com.jk.explore.locatorconsul.pattern;

import com.jk.explore.locatorconsul.consul.Address;

/** Ask for a service by name, get where to reach it. */
public interface Locator {

    Address find(String serviceName);
}
