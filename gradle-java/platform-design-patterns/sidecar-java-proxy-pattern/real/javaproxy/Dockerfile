# One class file, one JRE, nothing else.
#
# Compare this with ../payments/Dockerfile. They are the same four lines, and
# the jars they copy differ by about twenty megabytes: one carries a web
# framework and its dependency tree, and the other carries a single class that
# compiles against the JDK. That difference is one line of the bill in the
# README -- a JVM beside every service, where a few megabytes of nginx used to
# sit -- and it is smaller than the framework version would be but it is not
# nothing.
FROM eclipse-temurin:21-jre-alpine
WORKDIR /app
COPY build/libs/javaproxy.jar /app/javaproxy.jar
ENTRYPOINT ["java", "-jar", "/app/javaproxy.jar"]
