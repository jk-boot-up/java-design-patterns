package com.jk.explore.transactionaloutboxdebezium;

/**
 * One message as it sits in Kafka, read back by the demo.
 *
 * @param partition which of the topic's partitions it landed in
 * @param place     its numbered place in that partition, which Kafka calls the offset
 * @param orderId   the message key: the order it is about
 * @param type      what happened: OrderPlaced, OrderPaid or OrderShipped
 * @param eventId   the outbox row's id, carried as a header; the same every time the event is sent
 */
public record OrderEvent(int partition, long place, String orderId, String type, String eventId) {
}
