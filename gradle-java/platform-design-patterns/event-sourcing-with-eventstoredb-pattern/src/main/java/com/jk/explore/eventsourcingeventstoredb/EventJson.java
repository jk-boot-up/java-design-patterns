package com.jk.explore.eventsourcingeventstoredb;

import java.nio.charset.StandardCharsets;
import java.time.LocalDate;
import java.util.UUID;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import io.kurrent.dbclient.EventData;
import io.kurrent.dbclient.EventDataBuilder;
import io.kurrent.dbclient.RecordedEvent;

/**
 * Turns a loyalty event into what KurrentDB stores, and back.
 *
 * <p>KurrentDB stores each event as three things: an event type, which is a short name such as
 * PointsAwarded; the event's body, here a small piece of JSON text; and an event id, a random
 * identifier the writer chooses. The id matters more than it looks: the fourth act shows the
 * server using it to recognise a retry.
 *
 * <p>The JSON is written and read by hand, with no library, because the events have four
 * fields and a beginner should be able to read every character that crosses the network.
 */
public final class EventJson {

    private static final Pattern FIELD = Pattern.compile("\"(\\w+)\":\"?([^\",}]*)\"?");

    private EventJson() {
    }

    /** A new event with a fresh random id. */
    public static EventData toEventData(LoyaltyEvent event) {
        return toEventData(UUID.randomUUID(), event);
    }

    /** A new event with an id the caller chose, so that the same id can be sent again. */
    public static EventData toEventData(UUID eventId, LoyaltyEvent event) {
        return EventDataBuilder.json(eventId, typeOf(event), toJson(event).getBytes(StandardCharsets.UTF_8)).build();
    }

    public static String typeOf(LoyaltyEvent event) {
        return event.getClass().getSimpleName();
    }

    public static String toJson(LoyaltyEvent event) {
        String order = switch (event) {
            case PointsAwarded a -> ",\"orderId\":\"" + a.orderId() + "\"";
            case PointsRedeemed r -> ",\"orderId\":\"" + r.orderId() + "\"";
            case PointsExpired x -> "";
        };
        return "{\"customerId\":\"" + event.customerId() + "\",\"points\":" + event.points()
                + order + ",\"on\":\"" + event.on() + "\"}";
    }

    public static LoyaltyEvent fromRecorded(RecordedEvent recorded) {
        return fromJson(recorded.getEventType(), new String(recorded.getEventData(), StandardCharsets.UTF_8));
    }

    public static LoyaltyEvent fromJson(String type, String json) {
        String customer = field(json, "customerId");
        int points = Integer.parseInt(field(json, "points"));
        LocalDate on = LocalDate.parse(field(json, "on"));
        return switch (type) {
            case "PointsAwarded" -> new PointsAwarded(customer, points, field(json, "orderId"), on);
            case "PointsRedeemed" -> new PointsRedeemed(customer, points, field(json, "orderId"), on);
            case "PointsExpired" -> new PointsExpired(customer, points, on);
            default -> throw new IllegalArgumentException("not a loyalty event: " + type);
        };
    }

    private static String field(String json, String name) {
        Matcher m = FIELD.matcher(json);
        while (m.find()) {
            if (m.group(1).equals(name)) {
                return m.group(2);
            }
        }
        throw new IllegalArgumentException("no " + name + " in " + json);
    }
}
