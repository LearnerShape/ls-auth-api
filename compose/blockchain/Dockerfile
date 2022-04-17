# Part 1: Build the app
FROM gradle:7.4.2-jdk11 AS build
VOLUME /tmp
RUN mkdir /work
COPY --chown=gradle:gradle ./blockchain /work
WORKDIR /work
COPY .prism_password /.prism_password
RUN PRISM_SDK_PASSWORD=$(cat /.prism_password) gradle build --no-daemon


# Part 2: Run
FROM openjdk:11
RUN mkdir /app
COPY --from=build /work/build/libs/*SNAPSHOT.jar /app/spring-boot-application.jar
ENTRYPOINT ["java", "-XX:+UnlockExperimentalVMOptions", "-Djava.security.egd=file:/dev/./urandom","-jar","/app/spring-boot-application.jar"]