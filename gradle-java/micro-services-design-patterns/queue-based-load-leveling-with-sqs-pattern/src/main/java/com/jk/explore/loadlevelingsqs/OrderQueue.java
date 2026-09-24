package com.jk.explore.loadlevelingsqs;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import software.amazon.awssdk.services.sqs.SqsClient;
import software.amazon.awssdk.services.sqs.model.DeleteMessageBatchRequestEntry;
import software.amazon.awssdk.services.sqs.model.Message;
import software.amazon.awssdk.services.sqs.model.MessageSystemAttributeName;
import software.amazon.awssdk.services.sqs.model.QueueAttributeName;
import software.amazon.awssdk.services.sqs.model.SendMessageBatchRequestEntry;

/**
 * One queue on Amazon SQS, holding the orders checkout has accepted and the packing service
 * has not yet packed.
 *
 * <p>Three words carry the whole lesson, and each is said plainly here first.
 * <ul>
 *   <li><b>Waiting</b>: an order on the queue that nobody has taken yet.</li>
 *   <li><b>In flight</b>: an order a packer has taken but not yet finished. SQS still keeps
 *       it; it only hides it from everybody else.</li>
 *   <li><b>Visibility timeout</b>: how long SQS hides a taken order. When that time runs out
 *       and the order has not been deleted, SQS puts it back as waiting and hands it out
 *       again, to whoever asks next.</li>
 * </ul>
 */
public class OrderQueue {

    /** The most orders SQS takes in one send request, and hands out in one receive request. */
    public static final int MOST_PER_REQUEST = 10;

    /** An order a packer has taken: its id, the receipt needed to delete it, and how many times SQS has handed it out. */
    public record Taken(String orderId, String receipt, int timesHandedOut) {
    }

    private final SqsClient sqs;
    private final String url;

    private OrderQueue(SqsClient sqs, String url) {
        this.sqs = sqs;
        this.url = url;
    }

    /** A queue with SQS's defaults, including a visibility timeout of 30 seconds. */
    public static OrderQueue create(SqsClient sqs, String name) {
        return new OrderQueue(sqs, sqs.createQueue(b -> b.queueName(name)).queueUrl());
    }

    /** A queue that hides a taken order for the given number of seconds. */
    public static OrderQueue create(SqsClient sqs, String name, int visibilityTimeoutSeconds) {
        return new OrderQueue(sqs, sqs.createQueue(b -> b.queueName(name)
                .attributesWithStrings(Map.of("VisibilityTimeout", String.valueOf(visibilityTimeoutSeconds)))).queueUrl());
    }

    /** Asks SQS for a queue with any attributes at all. SQS refuses a name it does not know. */
    public static OrderQueue create(SqsClient sqs, String name, Map<String, String> attributes) {
        return new OrderQueue(sqs, sqs.createQueue(b -> b.queueName(name).attributesWithStrings(attributes)).queueUrl());
    }

    /** Sends these orders in one request. SQS refuses the whole request if there are more than 10. */
    public void sendTogether(List<String> orderIds) {
        List<SendMessageBatchRequestEntry> entries = new ArrayList<>();
        for (int i = 0; i < orderIds.size(); i++) {
            entries.add(SendMessageBatchRequestEntry.builder().id("n" + i).messageBody(orderIds.get(i)).build());
        }
        sqs.sendMessageBatch(b -> b.queueUrl(url).entries(entries));
    }

    /** Sends any number of orders, 10 to a request, and returns how many requests that took. */
    public int sendAll(List<String> orderIds) {
        int requests = 0;
        for (int from = 0; from < orderIds.size(); from += MOST_PER_REQUEST) {
            sendTogether(orderIds.subList(from, Math.min(from + MOST_PER_REQUEST, orderIds.size())));
            requests++;
        }
        return requests;
    }

    /** Sends one order in a request of its own. */
    public void sendOne(String orderId) {
        sqs.sendMessage(b -> b.queueUrl(url).messageBody(orderId));
    }

    /** Takes up to this many waiting orders, answering at once, possibly with none. */
    public List<Taken> take(int most) {
        return take(most, 0);
    }

    /**
     * Takes up to this many waiting orders. With a wait of more than zero seconds, SQS holds
     * the question open until an order is there or the time is up; SQS calls this long polling.
     */
    public List<Taken> take(int most, int waitSeconds) {
        List<Message> messages = sqs.receiveMessage(b -> b.queueUrl(url).maxNumberOfMessages(most).waitTimeSeconds(waitSeconds)
                .messageSystemAttributeNames(MessageSystemAttributeName.APPROXIMATE_RECEIVE_COUNT)).messages();
        List<Taken> taken = new ArrayList<>();
        for (Message m : messages) {
            int times = Integer.parseInt(m.attributes().get(MessageSystemAttributeName.APPROXIMATE_RECEIVE_COUNT));
            taken.add(new Taken(m.body(), m.receiptHandle(), times));
        }
        return taken;
    }

    /** Takes exactly one order, asking again until SQS hands one out. */
    public Taken takeOne() {
        Taken[] holder = new Taken[1];
        Poll.until("an order to be handed out", () -> {
            List<Taken> got = take(1);
            if (got.isEmpty()) {
                return false;
            }
            holder[0] = got.get(0);
            return true;
        });
        return holder[0];
    }

    /** Tells SQS this order is finished, so it may forget it. */
    public void delete(Taken order) {
        sqs.deleteMessage(b -> b.queueUrl(url).receiptHandle(order.receipt()));
    }

    /** Tells SQS these orders are finished, in one request. */
    public void deleteTogether(List<Taken> orders) {
        List<DeleteMessageBatchRequestEntry> entries = new ArrayList<>();
        for (int i = 0; i < orders.size(); i++) {
            entries.add(DeleteMessageBatchRequestEntry.builder().id("n" + i).receiptHandle(orders.get(i).receipt()).build());
        }
        sqs.deleteMessageBatch(b -> b.queueUrl(url).entries(entries));
    }

    /** Tells SQS the packer is still working on this order: hide it for this many more seconds, counted from now. */
    public void stillWorking(Taken order, int seconds) {
        sqs.changeMessageVisibility(b -> b.queueUrl(url).receiptHandle(order.receipt()).visibilityTimeout(seconds));
    }

    /** Orders nobody has taken, as SQS counts them. This is the depth of the queue. */
    public int waiting() {
        return number(QueueAttributeName.APPROXIMATE_NUMBER_OF_MESSAGES);
    }

    /** Orders taken but not yet deleted, as SQS counts them. */
    public int inFlight() {
        return number(QueueAttributeName.APPROXIMATE_NUMBER_OF_MESSAGES_NOT_VISIBLE);
    }

    public int visibilityTimeoutSeconds() {
        return number(QueueAttributeName.VISIBILITY_TIMEOUT);
    }

    /** How long SQS keeps an order nobody takes, in seconds, before it throws it away. */
    public int keepsUntakenSeconds() {
        return number(QueueAttributeName.MESSAGE_RETENTION_PERIOD);
    }

    private int number(QueueAttributeName attribute) {
        return Integer.parseInt(sqs.getQueueAttributes(b -> b.queueUrl(url).attributeNames(attribute)).attributes().get(attribute));
    }
}
