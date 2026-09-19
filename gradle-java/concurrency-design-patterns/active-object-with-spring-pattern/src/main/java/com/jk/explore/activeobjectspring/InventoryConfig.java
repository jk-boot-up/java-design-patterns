package com.jk.explore.activeobjectspring;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;

/**
 * <strong>The mailbox: one thread and a queue.</strong> The partner project, Active Object, wrote a class
 * with its own thread and queue. Here it is a bean. One thread is what makes the state safe without a lock,
 * so the pool must never have two.
 */
@Configuration
@EnableAsync
public class InventoryConfig {

    @Bean("inventoryExecutor")
    public ThreadPoolTaskExecutor inventoryExecutor(
            @Value("${inventory.mailbox-capacity:2147483647}") int mailboxCapacity) {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(1);
        executor.setMaxPoolSize(1);
        executor.setQueueCapacity(mailboxCapacity);
        executor.setThreadNamePrefix("inventory-");
        return executor;
    }
}
