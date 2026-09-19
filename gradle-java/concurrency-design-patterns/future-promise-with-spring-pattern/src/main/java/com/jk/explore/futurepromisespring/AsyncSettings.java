package com.jk.explore.futurepromisespring;

import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.task.TaskDecorator;
import org.springframework.scheduling.annotation.EnableAsync;

import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;

/** What the container does with the things a caller cannot see. */
@Configuration
@EnableAsync
public class AsyncSettings {

    /** Exceptions from {@code void} @Async methods, which would otherwise only be logged. */
    @Bean
    public List<String> uncaughtAsyncExceptions() {
        return new CopyOnWriteArrayList<>();
    }

    /** Copies the caller's customer onto the pool thread. Only present when {@code demo.propagate-context=true}. */
    @Bean
    @ConditionalOnProperty(name = "demo.propagate-context", havingValue = "true")
    public TaskDecorator customerContextDecorator() {
        return task -> {
            Integer customer = CustomerContext.get();
            return () -> {
                CustomerContext.set(customer);
                try {
                    task.run();
                } finally {
                    CustomerContext.clear();
                }
            };
        };
    }
}
