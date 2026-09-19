package com.jk.explore.futurepromisespring;

import org.springframework.aop.interceptor.AsyncUncaughtExceptionHandler;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.context.annotation.Lazy;
import org.springframework.scheduling.annotation.AsyncConfigurer;
import org.springframework.stereotype.Component;

import java.util.List;
import java.util.concurrent.Executor;

/**
 * <strong>The one place a void async method's exception can go.</strong> It is registered by hand. Without it,
 * Spring logs the exception and the caller never knows. It keeps Spring Boot's own executor.
 */
@Component
public class UncaughtHandler implements AsyncConfigurer {

    private final List<String> uncaught;
    private final Executor executor;

    public UncaughtHandler(@Qualifier("uncaughtAsyncExceptions") List<String> uncaught,
                           @Lazy @Qualifier("applicationTaskExecutor") Executor executor) {
        this.uncaught = uncaught;
        this.executor = executor;
    }

    @Override
    public Executor getAsyncExecutor() {
        return executor;
    }

    @Override
    public AsyncUncaughtExceptionHandler getAsyncUncaughtExceptionHandler() {
        return (throwable, method, params) -> uncaught.add(method.getName() + ": " + throwable.getMessage());
    }
}
