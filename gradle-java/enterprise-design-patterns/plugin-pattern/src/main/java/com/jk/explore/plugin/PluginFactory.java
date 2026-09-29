package com.jk.explore.plugin;

import java.io.IOException;
import java.io.InputStream;
import java.io.UncheckedIOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Properties;

/**
 * The pattern: reads which class implements each interface from the environment's configuration file, and creates it.
 *
 * <p>The file {@code plugins-<env>.properties} maps an interface's name to a
 * class name. The shop's code asks for the interface; this factory is the
 * only place that turns a class name into an object.
 */
public final class PluginFactory {

    private final String env;
    private final Properties config = new Properties();

    public PluginFactory(String env) {
        this.env = env;
        String file = "plugins-" + env + ".properties";
        try (InputStream in = PluginFactory.class.getClassLoader().getResourceAsStream(file)) {
            if (in == null) {
                throw new IllegalStateException("no configuration file " + file);
            }
            config.load(in);
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
    }

    public <T> T get(Class<T> type) {
        String className = config.getProperty(type.getSimpleName());
        if (className == null) {
            throw new IllegalStateException(env + ": no plugin configured for " + type.getSimpleName());
        }
        try {
            return type.cast(Class.forName(className).getDeclaredConstructor().newInstance());
        } catch (ReflectiveOperationException e) {
            throw new IllegalStateException(env + ": cannot create " + className + " for " + type.getSimpleName());
        }
    }

    /** Creates every configured plugin once, so a bad entry fails at startup, not at the first order. */
    public List<String> check(Class<?>... types) {
        List<String> problems = new ArrayList<>();
        for (Class<?> t : types) {
            try {
                get(t);
            } catch (IllegalStateException e) {
                problems.add(e.getMessage());
            }
        }
        return problems;
    }
}
