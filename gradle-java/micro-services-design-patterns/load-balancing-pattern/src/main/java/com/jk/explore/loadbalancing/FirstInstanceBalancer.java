package com.jk.explore.loadbalancing;

import java.util.List;

/**
 * Always call the first one on the list. The naive alternative.
 *
 * Nobody writes this deliberately; it is what you get by writing
 * {@code instances.get(0)} and moving on, and it is completely invisible in
 * testing, where there is one instance and the first one is the only one.
 *
 * <p>In production it concentrates every request on one box while the others idle,
 * which means the shop has bought three instances and is running on one. The
 * failure mode is not an error — it is a bill, and a machine that falls over under
 * load the other two could have absorbed.
 */
public final class FirstInstanceBalancer implements LoadBalancer {

    @Override
    public ServiceInstance choose(List<ServiceInstance> candidates) {
        return candidates.get(0);
    }

    @Override
    public String name() {
        return "first-on-the-list";
    }
}
