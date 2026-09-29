package com.jk.explore.spacehazelcast;

import com.hazelcast.config.Config;
import com.hazelcast.config.JoinConfig;
import com.hazelcast.config.MapConfig;
import com.hazelcast.config.MapStoreConfig;
import com.hazelcast.core.Hazelcast;
import com.hazelcast.core.HazelcastInstance;
import com.hazelcast.map.IMap;
import java.util.ArrayList;
import java.util.List;

/**
 * Three processing units, each a real Hazelcast cluster member running in this program, joined over
 * the local network. The stock map is split across them, with one backup copy of every entry.
 */
public final class Grid implements AutoCloseable {

    private final List<HazelcastInstance> units = new ArrayList<>();

    public Grid(int count, SlowDatabase database) {
        StockStore.database = database;
        for (int i = 0; i < count; i++) {
            units.add(Hazelcast.newHazelcastInstance(config()));
        }
    }

    private static Config config() {
        Config c = new Config();
        c.setClusterName("shop-" + ProcessHandle.current().pid());
        c.setProperty("hazelcast.logging.type", "none");
        c.setProperty("hazelcast.phone.home.enabled", "false");
        c.getNetworkConfig().setPort(5901).setPortAutoIncrement(true);
        JoinConfig join = c.getNetworkConfig().getJoin();
        join.getMulticastConfig().setEnabled(false);
        join.getAutoDetectionConfig().setEnabled(false);
        join.getTcpIpConfig().setEnabled(true).addMember("127.0.0.1");
        MapConfig stock = new MapConfig("stock").setBackupCount(1);
        stock.setMapStoreConfig(new MapStoreConfig()
                .setEnabled(true)
                .setImplementation(new StockStore())
                .setWriteDelaySeconds(2)       // write-behind: the database is written later, in the background
                .setWriteCoalescing(true));    // only the latest value of each key is written
        c.addMapConfig(stock);
        return c;
    }

    /** The stock map, as seen from one unit. */
    public IMap<String, Integer> stock(int i) {
        return units.get(i).getMap("stock");
    }

    public HazelcastInstance unit(int i) {
        return units.get(i);
    }

    public int members() {
        return units.get(0).getCluster().getMembers().size();
    }

    /** Stops one unit abruptly, as a crash would. */
    public void kill(int i) {
        units.get(i).getLifecycleService().terminate();
    }

    @Override
    public void close() {
        Hazelcast.shutdownAll();
    }
}
