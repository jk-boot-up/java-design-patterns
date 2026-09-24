package com.jk.explore.loadlevelingsqs;

import java.util.List;

/**
 * The packing service: the worker behind the queue. It keeps its own pace, which is at most
 * 10 orders a round, whatever is waiting.
 *
 * <p>A round is: take up to 10 orders, pack each one, then tell SQS they are finished by
 * deleting them. Deleting comes last on purpose. An order that is taken and never deleted is
 * not lost; SQS hands it out again when its visibility timeout runs out.
 */
public class Packer {

    private final OrderQueue queue;
    private final Warehouse warehouse;

    public Packer(OrderQueue queue, Warehouse warehouse) {
        this.queue = queue;
        this.warehouse = warehouse;
    }

    /** One round. Returns the orders it packed, which may be none. */
    public List<OrderQueue.Taken> round() {
        List<OrderQueue.Taken> taken = queue.take(OrderQueue.MOST_PER_REQUEST);
        for (OrderQueue.Taken order : taken) {
            warehouse.pack(order.orderId());
        }
        if (!taken.isEmpty()) {
            queue.deleteTogether(taken);
        }
        return taken;
    }
}
