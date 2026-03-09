# 📱 Mobile App Directory Structure

```text
mobile/
└── android-app/
    │
    ├── app/
    │   ├── src/
    │   │   ├── main/
    │   │   │
    │   │   │   ├── java/com/plantive/
    │   │   │   │
    │   │   │   │   ├── activities/
    │   │   │   │   │   ├── MainActivity.java
    │   │   │   │   │   ├── LoginActivity.java
    │   │   │   │   │   ├── RegisterActivity.java
    │   │   │   │   │
    │   │   │   │   ├── fragments/
    │   │   │   │   │   ├── HomeFragment.java
    │   │   │   │   │   ├── GardenFragment.java
    │   │   │   │   │   ├── MarketplaceFragment.java
    │   │   │   │   │   └── ProfileFragment.java
    │   │   │   │   │
    │   │   │   │   ├── adapters/
    │   │   │   │   │   ├── PlantAdapter.java
    │   │   │   │   │   └── ProductAdapter.java
    │   │   │   │   │
    │   │   │   │   ├── models/
    │   │   │   │   │   ├── User.java
    │   │   │   │   │   ├── Plant.java
    │   │   │   │   │   └── Product.java
    │   │   │   │   │
    │   │   │   │   ├── api/
    │   │   │   │   │   ├── ApiClient.java
    │   │   │   │   │   ├── ApiService.java
    │   │   │   │   │   └── AuthService.java
    │   │   │   │   │
    │   │   │   │   ├── repository/
    │   │   │   │   │   ├── AuthRepository.java
    │   │   │   │   │   ├── PlantRepository.java
    │   │   │   │   │   └── GardenRepository.java
    │   │   │   │   │
    │   │   │   │   ├── utils/
    │   │   │   │   │   ├── Constants.java
    │   │   │   │   │   ├── TokenManager.java
    │   │   │   │   │   └── DateUtils.java
    │   │   │   │   │
    │   │   │   │   └── services/
    │   │   │   │       └── NotificationService.java
    │   │   │   │
    │   │   │   ├── res/
    │   │   │   │   ├── layout/
    │   │   │   │   ├── drawable/
    │   │   │   │   ├── values/
    │   │   │   │   ├── menu/
    │   │   │   │   └── navigation/
    │   │   │   │
    │   │   │   └── AndroidManifest.xml
    │   │   │
    │   │   └── test/
    │   │
    │   ├── build.gradle
    │   └── proguard-rules.pro
    │
    ├── gradle/
    ├── build.gradle
    ├── settings.gradle
    └── README.md
```

---

# 📦 What Each Folder Does

## `activities/`

Main screens of the app.

Examples:

```
LoginActivity
RegisterActivity
MainActivity
```

`MainActivity` usually holds the **bottom navigation**.

---

# `fragments/`

Each tab of the app UI.

Example:

```
HomeFragment
GardenFragment
MarketplaceFragment
ProfileFragment
```

This keeps the UI modular.

---

# `adapters/`

RecyclerView adapters.

Examples:

```
PlantAdapter
ProductAdapter
```

Used to show lists like:

* plants
* marketplace items
* garden plants

---

# `models/`

Data models matching backend API.

Examples:

```
User
Plant
Product
GardenPlant
```

Example:

```java
public class Plant {
    private int id;
    private String plantName;
    private String soilType;
}
```

---

# `api/`

Handles **API communication with backend**.

Example:

```
ApiClient
ApiService
AuthService
```

Using **Retrofit** is recommended.

Example:

```java
@POST("/api/login")
Call<LoginResponse> login(@Body LoginRequest request);
```

---

# `repository/`

Acts as **data manager between API and UI**.

Example:

```
AuthRepository
PlantRepository
GardenRepository
```

Repositories make your code easier to maintain.

---

# `utils/`

Helper utilities.

Examples:

```
Constants
TokenManager
DateUtils
```

Example constant:

```java
public static final String BASE_URL = "http://10.0.2.2:3000/api/";
```

---

# `services/`

Background services.

Example:

```
NotificationService
```

Used for plant care reminders.

---

# `res/`

Android resources.

Important folders:

```
layout → XML UI
drawable → icons/images
values → colors, strings
menu → navigation menus
navigation → navigation graphs
```

---

# Example UI Screens for Your App

Your app might have:

```
Login
Register
Home Dashboard
My Garden
Plant Details
AI Chat
Marketplace
Profile
```

---