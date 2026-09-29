package com.jk.explore.blackboard;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * The shared board: facts about one order that any check can read and add to, plus a running risk score.
 */
public final class Blackboard {

    private final Map<String, String> facts = new LinkedHashMap<>();
    private final List<String> log = new ArrayList<>();
    private int risk;

    public Blackboard(Map<String, String> order) {
        facts.putAll(order);
    }

    public boolean has(String key) {
        return facts.containsKey(key);
    }

    public String get(String key) {
        return facts.get(key);
    }

    public void post(String who, String key, String value) {
        facts.put(key, value);
        log.add(who + ": " + key + "=" + value);
    }

    public void addRisk(String who, int points, String why) {
        risk += points;
        log.add(who + ": +" + points + " risk, " + why);
    }

    public int risk() {
        return risk;
    }

    public List<String> log() {
        return List.copyOf(log);
    }
}
