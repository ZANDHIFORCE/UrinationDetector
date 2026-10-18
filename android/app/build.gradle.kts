plugins {
    id("com.android.application")
}

// 로컬 서버 주소와 토큰은 빌드할 때 지정
val apiUrl = providers.environmentVariable("URINATION_API_URL").orElse("http://10.0.2.2:8000")
val apiToken = providers.environmentVariable("URINATION_API_TOKEN").orElse("")
fun quoted(value: String) = "\"" + value.replace("\\", "\\\\").replace("\"", "\\\"") + "\""

android {
    buildFeatures { buildConfig = true }
    namespace = "com.example.urnationdetector"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.example.urnationdetector"
        minSdk = 29
        targetSdk = 31
        versionCode = 1
        versionName = "1.0"
        buildConfigField("String", "API_URL", quoted(apiUrl.get().trimEnd('/')))
        buildConfigField("String", "API_TOKEN", quoted(apiToken.get()))

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_1_8
        targetCompatibility = JavaVersion.VERSION_1_8
    }
}

dependencies {

    implementation("androidx.appcompat:appcompat:1.6.1")
    implementation("com.google.android.material:material:1.10.0")
    implementation("androidx.constraintlayout:constraintlayout:2.1.4")
    testImplementation("junit:junit:4.13.2")
    androidTestImplementation("androidx.test.ext:junit:1.1.5")
    androidTestImplementation("androidx.test.espresso:espresso-core:3.5.1")
}