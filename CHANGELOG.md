# Changelog – Plantive 🌱

All notable changes to this project will be documented here.  
This follows **[Keep a Changelog](https://keepachangelog.com/en/1.0.0/)** conventions.

---

## [v0.3.0] – 12-03-2026

### Added

* **AI Fertilizer Recommendation API** (`/ai/fertilizer/`)

  * Returns top N fertilizer recommendations based on plant type, soil, sunlight, nutrients, and location
  * Includes detailed probability and description for each recommendation
  * Fully documented with Swagger UI examples
  * Request and response validated using Pydantic models
  * Logging added for requests, responses, and warnings

### Changed

* Updated project folder structure for AI service
* Added Pydantic request and response models for fertilizer recommendation

### Fixed

* Error handling added for cases with no recommendations found

---

## [v0.2.0] – 09-03-2026

### Added
- Web UI: Home screen dashboard
- AI scanner page (mock data)
- Project board setup
- Basic Git workflow for team

### Changed
- Folder structure organized for Web, Backend, AI, Database, Docs
- Update Readme

### Fixed
- Initial repository setup issues

---

## [v0.1.0] – 09-03-2026
### Added
- Repository created
- Main branch initialized
- Contributor guidelines drafted (`CONTRIBUTING.md`)
- Project Board columns created: `Todo`, `In Progress`, `Review`, `Done`