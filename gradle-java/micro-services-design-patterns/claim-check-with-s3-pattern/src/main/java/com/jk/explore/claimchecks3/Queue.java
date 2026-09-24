package com.jk.explore.claimchecks3;

import java.util.List;
import software.amazon.awssdk.services.sqs.SqsClient;
import software.amazon.awssdk.services.sqs.model.Message;
import software.amazon.awssdk.services.sqs.model.QueueAttributeName;

/**
 * One queue on Amazon SQS: the channel the shop's checkout uses to hand work to the email
 * service.
 *
 * <p>A message on SQS is text, and SQS has a hard limit on how long that text may be. The
 * limit is the whole reason this project exists: it is not a setting of this program, it is a
 * rule of the service, and the service enforces it by refusing the send.
 */
public class Queue {

    /** A message taken off the queue, and the receipt needed to tell SQS it was handled. */
    public record Received(String body, String receipt) {
    }

    private final SqsClient sqs;
    private final String name;
    private final String url;

    private Queue(SqsClient sqs, String name, String url) {
        this.sqs = sqs;
        this.name = name;
        this.url = url;
    }

    /** Creates the queue, or finds it if it already exists. */
    public static Queue create(SqsClient sqs, String name) {
        return new Queue(sqs, name, sqs.createQueue(b -> b.queueName(name)).queueUrl());
    }

    /**
     * A queue that was never created, addressed by a mistyped name. Sending to it fails the
     * way a send fails when the queue service cannot be reached: after the caller has already
     * done whatever it did first.
     */
    public static Queue missing(SqsClient sqs, Queue real) {
        return new Queue(sqs, real.name + "-typo", real.url + "-typo");
    }

    public String name() {
        return name;
    }

    /** Puts one text message on the queue. SQS refuses it, with an exception, if it is too long. */
    public void send(String text) {
        sqs.sendMessage(b -> b.queueUrl(url).messageBody(text));
    }

    /**
     * Takes one message, waiting up to a second for one to arrive. SQS hides a message it has
     * handed out for a while, so nobody else is given it, but keeps it until it is deleted.
     */
    public Received receiveOne() {
        List<Message> messages = sqs.receiveMessage(b -> b.queueUrl(url).maxNumberOfMessages(1).waitTimeSeconds(1)).messages();
        if (messages.isEmpty()) {
            return null;
        }
        return new Received(messages.get(0).body(), messages.get(0).receiptHandle());
    }

    /** Takes one message, polling until there is one. */
    public Received take() {
        Received[] holder = new Received[1];
        Poll.until("a message on " + name, () -> (holder[0] = receiveOne()) != null);
        return holder[0];
    }

    /** Tells SQS the message was handled, so it may forget it. */
    public void delete(Received received) {
        sqs.deleteMessage(b -> b.queueUrl(url).receiptHandle(received.receipt()));
    }

    /** How many messages are waiting to be taken, as SQS counts them. */
    public int waiting() {
        return Integer.parseInt(attribute(QueueAttributeName.APPROXIMATE_NUMBER_OF_MESSAGES));
    }

    /** The longest message this queue accepts, in bytes, as SQS reports it. */
    public int maximumMessageBytes() {
        return Integer.parseInt(attribute(QueueAttributeName.MAXIMUM_MESSAGE_SIZE));
    }

    /** How long SQS keeps a message nobody has taken, in seconds, as SQS reports it. */
    public int keepsUnreadSeconds() {
        return Integer.parseInt(attribute(QueueAttributeName.MESSAGE_RETENTION_PERIOD));
    }

    private String attribute(QueueAttributeName attribute) {
        return sqs.getQueueAttributes(b -> b.queueUrl(url).attributeNames(attribute)).attributes().get(attribute);
    }
}
