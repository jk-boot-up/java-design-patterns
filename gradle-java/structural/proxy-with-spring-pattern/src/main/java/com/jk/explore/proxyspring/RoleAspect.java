package com.jk.explore.proxyspring;

import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.springframework.stereotype.Component;

/**
 * The protection proxy, written once. Spring wraps every bean that has a method with
 * {@link RequiresRole} in a generated subclass, and that subclass runs this advice first.
 */
@Aspect
@Component
public class RoleAspect {

    private final Session session;

    public RoleAspect(Session session) {
        this.session = session;
    }

    @Around("@annotation(required)")
    public Object check(ProceedingJoinPoint call, RequiresRole required) throws Throwable {
        if (session.role() != required.value()) {
            throw new AccessDenied(call.getSignature().getName() + " needs " + required.value()
                    + " but the caller is " + session.role());
        }
        return call.proceed();
    }
}
