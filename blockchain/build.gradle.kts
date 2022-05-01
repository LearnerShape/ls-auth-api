import org.jetbrains.kotlin.gradle.tasks.KotlinCompile

plugins {
	id("org.springframework.boot") version "2.6.5"
	id("io.spring.dependency-management") version "1.0.11.RELEASE"
	kotlin("jvm") version "1.5.0"
	kotlin("plugin.spring") version "1.6.10"
}

group = "com.example"
version = "0.0.1-SNAPSHOT"
java.sourceCompatibility = JavaVersion.VERSION_11

repositories {
	mavenCentral()
  mavenLocal()
  google()
  maven("https://plugins.gradle.org/m2/")
  maven {
    url = uri("https://maven.pkg.github.com/input-output-hk/better-parse")
      credentials {
            username = "atala-dev"
            password = System.getenv("PRISM_SDK_PASSWORD")
      }
  }
}

dependencies {
  // Align versions of all Kotlin components
  implementation(platform("org.jetbrains.kotlin:kotlin-bom"))

	implementation("org.springframework.boot:spring-boot-starter-web")
	implementation("com.fasterxml.jackson.module:jackson-module-kotlin")
	implementation("org.jetbrains.kotlin:kotlin-reflect")
	implementation("org.jetbrains.kotlin:kotlin-stdlib-jdk8")

  // needed for cryptography primitives implementation
  implementation("io.iohk.atala:prism-crypto:v1.3.2")

  // needed to deal with DIDs
  implementation("io.iohk.atala:prism-identity:v1.3.2")

  // needed to deal with credentials
  implementation("io.iohk.atala:prism-credentials:v1.3.2")

  // needed to interact with PRISM Node service
  implementation("io.iohk.atala:prism-api:v1.3.2")

  // needed for the credential content, bring the latest version
  implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.2.2")

  // needed for dealing with dates, bring the latest version
  implementation("org.jetbrains.kotlinx:kotlinx-datetime:0.2.1")

  // Fixes a bug from SLF4J
  // Seems to cause an issue
  // implementation("org.slf4j:slf4j-simple:1.7.32")

  // Fixes a build issue
  implementation("com.soywiz.korlibs.krypto:krypto-jvm:2.0.6")

  testImplementation("org.springframework.boot:spring-boot-starter-test")
}

// tasks.withType<KotlinCompile> {
// 	kotlinOptions {
// 		freeCompilerArgs = listOf("-Xjsr305=strict")
// 		jvmTarget = "11"
// 	}
// }

tasks.withType<Test> {
	useJUnitPlatform()
}

