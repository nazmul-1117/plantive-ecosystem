
# Contributing to Plantive 🌱

Thank you for your interest in contributing! This guide will help you **work efficiently in a team** and avoid mistakes.

---

## 1️⃣ Getting Started

1. **Clone the repository**:

```bash
git clone https://github.com/nazmul-1117/plantive-ecosystem.git
````

2. **Create your own branch** for any new feature or bugfix:

```bash
git checkout -b feature/your-feature-name
```

3. **Sync with develop** before starting:

```bash
git checkout develop
git pull origin develop
```

---

## 2️⃣ Branch Workflow

* **main** – Stable production code (Leader only merges here)
* **develop** – Integration branch (all features merge here first)
* **feature/** – Your individual feature or bugfix branch

**Example:**

```text
feature/web-ui
feature/backend-api
feature/ai-service
feature/fertilizer
feature/community
```

---

## 3️⃣ Commit Guidelines

Use **descriptive commit messages**:

```text
feat: add plant dashboard UI (#1)
fix: correct login bug (#2)
ui: improve home page layout
docs: update README
```

* Include the **issue number** to automatically link commits to tasks: `Closes #1`

---

## 4️⃣ Pull Requests (PR)

1. Push your branch:

```bash
git push origin feature/your-feature
```

2. Open a **Pull Request** to merge into `develop` (or `main` if approved).
3. PR checklist:

* [ ] Code works locally
* [ ] No errors/warnings
* [ ] Linked to an Issue
* [ ] Follows commit style
* [ ] UI matches design (if applicable)

4. Wait for **review and approval** from the leader before merging.

---

## 5️⃣ Project Board & Issues

* Check **Project Board** to see tasks: `Todo → In Progress → Review → Done`
* Move cards as you progress:

  * Start working → **In Progress**
  * Work finished → **Review**
  * Leader approves → **Done**

---

## 6️⃣ Folder Structure

```text
web/       → frontend / Web UI
backend/   → backend API
ai-service/→ AI modules
database/  → schema & data
docs/      → documentation
```

---

## 7️⃣ Communication

* Use **GitHub Issues** for questions or bugs
* Ask the team leader before making structural changes to the repository

---

> Following this workflow keeps Plantive clean, organized, and professional like a real startup. 🚀