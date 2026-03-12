# SPRINT 36 - Consolidated Task List

This document outlines the detailed tasks for Sprint 36, organized by Epic. The definitions are structured using high industry standard practices, including clear context, acceptance criteria, effort estimates, and technical implementation notes.

---

## EPIC 1: Conditional change OLD VS NEW IDP
**Objective:** Support dynamic switching and conditional token verification between the legacy IDP and the new IDP.

### TASK 1.1: Conditional Change SAML FLOW (LMS)
* **Assignee:** Rakesh
* **Estimate:** 1.5 Days
* **Status:** To Do

**📖 User Story / Context**
* **As a:** System User / Administrator
* **I want to:** Authenticate correctly via the appropriate SAML flow (Old vs. New IDP) based on environment flags or account settings.
* **So that:** The Learning Management System (LMS) seamlessly supports users on both the legacy and new Identity Providers.

**✅ Acceptance Criteria**
* [ ] Implement routing logic to direct SAML login requests to the New IDP if the feature flag/setting is active.
* [ ] Retain and route to the Old IDP SAML flow for accounts that have not yet migrated.
* [ ] After successful IDP authentication, the user is redirected back to the LMS accurately and a session is created.

**🛠 Technical Implementation Notes**
* Check identity provider configuration settings before triggering the SAML Assertion.
* Update `AuthService` to cleanly handle both SAML response models.

---

### TASK 1.2: OLD API token verification - Conditional for NEW IDP and OLD IDP token
* **Assignee:** Rakesh
* **Estimate:** 1.5 Days
* **Status:** To Do

**📖 User Story / Context**
* **As a:** Backend API Service
* **I want to:** Conditionally verify access tokens issued by both Old and New Identity Providers.
* **So that:** API endpoints remain secure and accessible regardless of which IDP issued the user's token.

**✅ Acceptance Criteria**
* [ ] API Middleware accurately determines if an incoming JWT belongs to the Old or New IDP (e.g., via `iss` claim or custom header).
* [ ] If it is a New IDP token, validate it against the New IDP's JWKS endpoint/secret.
* [ ] If it is an Old IDP token, validate using the legacy secret mechanism.
* [ ] Deny requests containing invalid tokens and return a standard `401 Unauthorized` response.

---

## EPIC 2: Student Dashboard
**Objective:** Enhance session stability for students authenticated via the new IDP.

### TASK 2.1: Refresh Token Implementation (Interceptor) for New IDP
* **Assignee:** Bhasker
* **Estimate:** 1.5 Days
* **Status:** To Do

**📖 User Story / Context**
* **As a:** Student
* **I want to:** Have my session silently extended in the background without unexpected logouts.
* **So that:** My learning experience on the dashboard is continuous and uninterrupted.

**✅ Acceptance Criteria**
* [ ] Implement an Axios/HTTP Interceptor on the Student Dashboard frontend that catches `401 Unauthorized` responses.
* [ ] Automatically trigger a background call to the new IDP refresh token endpoint upon interception.
* [ ] If refresh succeeds, retrieve the new access token and retry the originally failed HTTP request seamlessly.
* [ ] If refresh fails (refresh token is expired/invalid), clear local session data and cleanly redirect the user to the login screen.

---

## EPIC 3: OLD IDP functionality migrate
**Objective:** Decommission legacy IAM dependencies by migrating core functionalities to the New IDP.

### TASK 3.1: NEW IDP - User Management Finalize (LMS, TMS, Student Dashboard)
* **Assignee:** Rakesh
* **Estimate:** 2 Days
* **Status:** To Do

**📖 User Story / Context**
* **As a:** Platform Administrator
* **I want to:** Have user management fully integrated with the New IDP across LMS, TMS, and the Student Dashboard.
* **So that:** I can manage users from a single source of truth without relying on legacy systems.

**✅ Acceptance Criteria**
* [ ] Verify that user creation, updates, and soft-deletes synchronize properly with the New IDP.
* [ ] Ensure that roles and permissions mapped in LMS/TMS correspond accurately to the New IDP claims.
* [ ] Resolve any existing bugs related to profile data sync between the active services and the New IDP.

**🛠 Technical Implementation Notes**
* **Testing:** Required end-to-end testing of full user lifecycle state changes (Create -> Update -> Suspend -> Delete).

---

### TASK 3.2: SP Update
* **Assignee:** Rakesh
* **Estimate:** 1 Day
* **Status:** Skipped (Not in current scope)

---

### TASK 3.3: LTI
* **Assignee:** Rakesh
* **Estimate:** 1 Day
* **Status:** Skipped (Not in current scope)

---

### TASK 3.4: Subscription (Chargebee)
* **Status:** Skipped (Not in current scope)

---

### TASK 3.5: Onboarding
* **Status:** Skipped (Not in current scope)

---

## EPIC 4: Generate Auth Token
**Objective:** Establish a robust centralized mechanism for generating and distributing API Gateway authentication tokens.

### TASK 4.1: Generate Auth Token (Complete rewrite on API Gateway - VLE Admin)
* **Estimate:** 3 Days
* **Status:** To Do

**📖 User Story / Context**
* **As a:** VLE Administrator / API Client
* **I want to:** Request a secure authentication token directly from the API Gateway.
* **So that:** Automated services and integrations can securely authenticate against VLE Admin APIs using standard protocols.

**✅ Acceptance Criteria**
* [ ] Completely rewrite the token generation logic to reside on the API Gateway layer.
* [ ] The specialized endpoint consumes secure client credentials and returns a secure, signed JWT.
* [ ] The generated token includes strict scopes/claims necessary for VLE Admin privileges.

---

### TASK 4.2: Implement on respective SPs (MYkademy, StudentDashboard, DMS, TMS, E-portfolio)
* **Estimate:** 1 Day
* **Status:** To Do

**✅ Acceptance Criteria**
* [ ] All integrated Service Providers can successfully invoke the new Auth Token utility to process service-to-service calls.
* [ ] Clean up and deprecate any legacy token-request endpoints within these platforms.

---

### TASK 4.3: Write New API for other data (Allowed products, analytics, S3 URLs, tilezone, etc.)
* **Estimate:** 1 Day
* **Status:** To Do

**✅ Acceptance Criteria**
* [ ] Develop new Unified APIs on the Gateway to reliably deliver configuration and operational data (e.g., S3 pre-signed URLs, allowed products lists, analytics metadata).
* [ ] Ensure all endpoints are protected and validate against the newly established Auth Token verification logic.

---

## EPIC 5: Setting
**Objective:** Standardize how global configurations are managed across the system.

### TASK 5.1: Global Setting - VLE ADMIN (flag)
* **Status:** To Do

**📖 User Story / Context**
* **As a:** VLE Administrator
* **I want to:** Quickly toggle global configuration flags from the VLE Admin interface.
* **So that:** Operational changes (e.g., IDP switch override, maintenance modes) propagate platform-wide dynamically.

**✅ Acceptance Criteria**
* [ ] Implement API logic on VLE Admin to set, get, and securely expose global configuration flags.
* [ ] Ensure updates to global flags cascade efficiently (e.g., via Redis caching) and take effect without container restarts.
