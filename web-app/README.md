# Recommended `web/` Directory Structure

```text
├── web
│   └── api-tester
│       │
│       ├── public
│       │   ├── index.html
│       │   ├── login.html
│       │   ├── plants.html
│       │   ├── ai-test.html
│       │
│       ├── css
│       │   └── styles.css
│       │
│       ├── js
│       │   ├── api.js
│       │   ├── auth.js
│       │   ├── plants.js
│       │   └── ai.js
│       │
│       ├── config
│       │   └── apiConfig.js
│       │
│       └── README.md
```

---

# What Each Web Folder Does

## `public/`

Frontend pages for testing APIs.

Example:

```text
index.html       → dashboard
login.html       → test login API
plants.html      → test plant APIs
ai-test.html     → test AI endpoints
```

Example `login.html`:

```html
<input id="email" placeholder="email">
<input id="password" type="password">
<button onclick="login()">Login</button>
```

---

# `css/`

Styles for the web tester.

```text
styles.css
```

Just simple UI.

---

# `js/`

JavaScript that communicates with backend APIs.

Example files:

```text
api.js
auth.js
plants.js
ai.js
```

Example:

### `api.js`

```javascript
const BASE_URL = "http://localhost:3000/api";

async function apiRequest(endpoint, method="GET", body=null){
    const response = await fetch(BASE_URL + endpoint,{
        method: method,
        headers: {
            "Content-Type": "application/json"
        },
        body: body ? JSON.stringify(body) : null
    });

    return response.json();
}
```

---

### `auth.js`

```javascript
async function login(){
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const result = await apiRequest("/login","POST",{email,password});
    console.log(result);
}
```

---

# `config/`

Stores API base URLs.

```text
apiConfig.js
```

Example:

```javascript
export const API_BASE = "http://localhost:3000/api";
```

---

# Why This Web App is Useful

Your **web tester** helps you:

✔ Debug backend
✔ Test APIs quickly
✔ Show teachers a working interface
✔ Verify AI endpoints

Instead of using **Postman**, you have your own UI.

Example pages:

```text
Login Tester
Plant List Tester
Garden API Tester
AI Chat Tester
Disease Detection Tester
```

---

# Example API Flow

```
Web Tester
     │
     │ HTTP
     ▼
Node.js API
     │
     ▼
Database
     │
     ▼
Python AI Service
```

---

# Pro Tip (Very Useful)

Add this **web dashboard page**:

```text
/api-dashboard
```

Show buttons like:

```
[ Test Login ]
[ Get Plants ]
[ Add Garden Plant ]
[ AI Chat ]
[ Detect Disease ]
```

This will make your project look **like a real developer tool**.

---