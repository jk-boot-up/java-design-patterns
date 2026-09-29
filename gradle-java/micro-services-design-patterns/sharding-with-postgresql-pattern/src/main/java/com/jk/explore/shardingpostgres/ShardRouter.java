package com.jk.explore.shardingpostgres;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.util.ArrayList;
import java.util.List;

/**
 * The pattern: decides which database holds each customer, and sends every query there. A question
 * about one customer goes to one shard; a question about everyone goes to all of them.
 */
public final class ShardRouter {

    private final Shards shards;
    private int shardsAsked;

    public ShardRouter(Shards shards) {
        this.shards = shards;
    }

    public int shardFor(int customer) {
        return customer % shards.size();
    }

    public void placeOrder(int customer, String id, int pence) throws Exception {
        try (Connection c = shards.connect(shardFor(customer));
             PreparedStatement p = c.prepareStatement("INSERT INTO orders VALUES (?, ?, ?)")) {
            p.setString(1, id);
            p.setInt(2, customer);
            p.setInt(3, pence);
            p.executeUpdate();
        }
    }

    /** Many orders at once, grouped by shard, one batch per shard. */
    public void placeOrders(int count) throws Exception {
        for (int shard = 0; shard < shards.size(); shard++) {
            try (Connection c = shards.connect(shard);
                 PreparedStatement p = c.prepareStatement("INSERT INTO orders VALUES (?, ?, ?)")) {
                for (int customer = 1; customer <= count; customer++) {
                    if (shardFor(customer) == shard) {
                        p.setString(1, "ORD-" + customer);
                        p.setInt(2, customer);
                        p.setInt(3, PostgresShardingDemo.pence(customer));
                        p.addBatch();
                    }
                }
                p.executeBatch();
            }
        }
    }

    public int count(int shard) throws Exception {
        try (Connection c = shards.connect(shard);
             ResultSet r = c.createStatement().executeQuery("SELECT count(*) FROM orders")) {
            r.next();
            return r.getInt(1);
        }
    }

    public List<String> ordersOf(int customer) throws Exception {
        shardsAsked = 1;
        List<String> out = new ArrayList<>();
        try (Connection c = shards.connect(shardFor(customer));
             PreparedStatement p = c.prepareStatement("SELECT id FROM orders WHERE customer = ?")) {
            p.setInt(1, customer);
            try (ResultSet r = p.executeQuery()) {
                while (r.next()) {
                    out.add(r.getString(1));
                }
            }
        }
        return out;
    }

    /** Asks every shard the same question and adds the answers together. */
    public int countOver(int pence) throws Exception {
        shardsAsked = 0;
        int total = 0;
        for (int shard = 0; shard < shards.size(); shard++) {
            shardsAsked++;
            try (Connection c = shards.connect(shard);
                 PreparedStatement p = c.prepareStatement("SELECT count(*) FROM orders WHERE pence > ?")) {
                p.setInt(1, pence);
                try (ResultSet r = p.executeQuery()) {
                    r.next();
                    total += r.getInt(1);
                }
            }
        }
        return total;
    }

    /** Records a one-use coupon on the customer's shard. Returns whether the database accepted it. */
    public boolean redeem(String coupon, int customer) throws Exception {
        try (Connection c = shards.connect(shardFor(customer));
             PreparedStatement p = c.prepareStatement("INSERT INTO redemptions VALUES (?, ?)")) {
            p.setString(1, coupon);
            p.setInt(2, customer);
            p.executeUpdate();
            return true;
        } catch (java.sql.SQLException duplicate) {
            return false;
        }
    }

    public int shardsAsked() {
        return shardsAsked;
    }
}
