package com.jk.explore.roleobject;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Optional;
import java.util.Set;
import java.util.stream.Collectors;

/**
 * The pattern's core: one account, one identity, that can take on and drop roles while it lives.
 */
public final class Account {

    private final String id;
    private final String name;
    private final Map<Class<? extends Role>, Role> roles = new LinkedHashMap<>();

    public Account(String id, String name) {
        this.id = id;
        this.name = name;
    }

    public <T extends Role> T addRole(T role) {
        roles.put(role.getClass(), role);
        return role;
    }

    public void removeRole(Class<? extends Role> type) {
        roles.remove(type);
    }

    /** This account in the given role, or empty if it does not play that role right now. */
    public <T extends Role> Optional<T> as(Class<T> type) {
        return Optional.ofNullable(type.cast(roles.get(type)));
    }

    public Set<String> roleNames() {
        return roles.keySet().stream().map(Class::getSimpleName)
                .collect(Collectors.toCollection(java.util.LinkedHashSet::new));
    }

    public String id() {
        return id;
    }

    public String name() {
        return name;
    }
}
