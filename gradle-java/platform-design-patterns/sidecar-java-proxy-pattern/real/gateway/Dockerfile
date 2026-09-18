# One jar, one JRE, nothing else.
#
# The image is built from a jar Gradle has already produced rather than by
# running Gradle inside Docker, because a reader waiting four minutes for a
# container to download the internet learns nothing about sidecars. demo.sh
# runs ../gradlew bootJar first, and this copies what it made.
FROM eclipse-temurin:21-jre-alpine
WORKDIR /app
COPY build/libs/gateway.jar /app/gateway.jar
ENTRYPOINT ["java", "-jar", "/app/gateway.jar"]
