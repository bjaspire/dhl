# EPIC: Single Logout (SLO)

**Epic Duration:** 4 Days  
**Sprint:** SPRINT 35  
**Priority:** High  
**Epic Owner:** [Assign to Team Lead]

---

## Epic Description
Implement comprehensive Single Logout (SLO) functionality across the Identity Provider (IDP) and Service Providers (SP) to ensure secure and complete user session termination. This includes SAML-based logout, token invalidation, and session tracking mechanisms.

---

## Tasks

### TASK 1: Individual SP Logout Mechanism
**Estimate:** 1 Day

h2. 📖 User Story / Context
* **As a:** System Administrator
* **I want to:** Implement logout mechanism for individual Service Providers
* **So that:** Users can securely logout from specific services without affecting other active sessions

---

h2. ✅ Acceptance Criteria (Definition of Done)

* [ ] **Scenario 1:** User initiates logout from a specific SP
   * Given User is authenticated on multiple SPs
   * When User clicks logout on one SP
   * Then Only that SP session is terminated, other sessions remain active
* [ ] **Scenario 2:** Logout triggers proper cleanup
   * Given User initiates SP logout
   * When Logout request is processed
   * Then All SP-specific tokens and cookies are invalidated
* [ ] **Performance:** Logout completes within < 1 second
* [ ] **Security:** No session remnants remain after logout
* [ ] **Logging:** Logout events are properly logged with timestamp and user info

---

h2. 🛠 Technical Implementation Notes
* **API Endpoint:** `POST /api/v1/sp/logout`
* **Required Headers:** `Authorization: Bearer <token>`, `X-SP-ID: <service-provider-id>`
* **Database Changes:** None required
* **Security:** 
  - Validate token before processing logout
  - Clear session from Redis cache
  - Invalidate JWT tokens
* **Components:** 
  - `AuthService.logout()`
  - `SessionManager.clearSPSession()`

---

h2. 🧪 QA & Test Data
* **Test Environment:** `Development`, `Staging`
* **Test User Accounts:**
   * Standard User: `testuser@example.com` / `Test@123`
   * Admin: `admin@example.com` / `Admin@123`
* **Pre-requisites:** 
  - User must be logged into at least 2 different SPs
  - Active sessions in Redis

---

h2. 📎 Resources & Attachments
* **Related Tickets:** Part of SLO Epic
* **Documentation:** [SAML 2.0 Single Logout Specification](https://docs.oasis-open.org/security/saml/)

---

### TASK 2: IDP Logout Implementation
**Estimate:** 1 Day

h2. 📖 User Story / Context
* **As a:** Identity Provider Administrator
* **I want to:** Implement centralized IDP logout functionality
* **So that:** All connected Service Providers are notified and sessions are terminated globally

---

h2. ✅ Acceptance Criteria (Definition of Done)

* [ ] **Scenario 1:** IDP-initiated global logout
   * Given User is authenticated across multiple SPs via IDP
   * When User initiates logout from IDP
   * Then All SP sessions are terminated simultaneously
* [ ] **Scenario 2:** SAML logout request propagation
   * Given IDP receives logout request
   * When IDP processes the request
   * Then SAML LogoutRequest is sent to all registered SPs
* [ ] **Scenario 3:** SP logout response handling
   * Given IDP sent LogoutRequest to multiple SPs
   * When SPs respond with LogoutResponse
   * Then IDP validates all responses and confirms global logout
* [ ] **Performance:** IDP logout completes within < 3 seconds for up to 10 SPs
* [ ] **Error Handling:** If any SP fails to respond, IDP still completes logout with warning log

---

h2. 🛠 Technical Implementation Notes
* **API Endpoints:** 
  - `POST /api/v1/idp/logout` - Initiate IDP logout
  - `POST /api/v1/idp/saml/logout-request` - Send SAML logout to SPs
  - `POST /api/v1/idp/saml/logout-response` - Receive SP logout confirmations
* **Database Changes:** None required
* **Security:** 
  - Validate SAML LogoutRequest signature
  - Ensure logout request originates from authenticated session
  - Implement timeout mechanism (max 5s wait per SP)
* **Components:** 
  - `IDPAuthService.globalLogout()`
  - `SAMLService.sendLogoutRequest()`
  - `SAMLService.validateLogoutResponse()`

---

h2. 🧪 QA & Test Data
* **Test Environment:** `Staging`
* **Test User Accounts:**
   * User with multiple SP sessions: `multiuser@example.com` / `Test@123`
* **Pre-requisites:** 
  - At least 3 registered SPs with active SAML configuration
  - Active user sessions across all SPs

---

h2. 📎 Resources & Attachments
* **Related Tickets:** Depends on Task 1
* **SAML Spec:** [SAML 2.0 Bindings](https://www.oasis-open.org/committees/download.php/35387/sstc-saml-bindings-errata-2.0-wd-06-diff.pdf)

---

### TASK 3: Token Blacklisting (Access & Refresh Tokens)
**Estimate:** 1 Day

h2. 📖 User Story / Context
* **As a:** Security Engineer
* **I want to:** Blacklist access and refresh tokens upon logout
* **So that:** Logged-out users cannot use old tokens to access protected resources

---

h2. ✅ Acceptance Criteria (Definition of Done)

* [ ] **Scenario 1:** Token added to blacklist on logout
   * Given User initiates logout
   * When Logout is processed
   * Then Both access token and refresh token are added to Redis blacklist with TTL
* [ ] **Scenario 2:** Blacklisted token rejected
   * Given Token is in blacklist
   * When User attempts to use blacklisted token
   * Then Request is rejected with 401 Unauthorized and message "Token has been revoked"
* [ ] **Scenario 3:** Token expiry cleanup
   * Given Tokens have natural expiry time
   * When Token TTL expires in blacklist
   * Then Redis automatically removes the entry
* [ ] **Performance:** Token validation (including blacklist check) < 50ms
* [ ] **Storage:** Blacklist uses Redis with efficient memory usage

---

h2. 🛠 Technical Implementation Notes
* **Database Changes:** 
  - Use Redis for token blacklist
  - Key format: `blacklist:token:<jti>`
  - Value: `{userId, logoutTimestamp, reason}`
  - TTL: Match token expiry time
* **Security:** 
  - Store only token JTI (JWT ID), not full token
  - Implement rate limiting on token validation
* **Components:** 
  - `TokenBlacklistService.add(token)`
  - `TokenBlacklistService.isBlacklisted(token)`
  - `AuthMiddleware.validateToken()` - Updated to check blacklist
* **API Updates:**
  - All protected endpoints must validate against blacklist

---

h2. 🧪 QA & Test Data
* **Test Environment:** `Development`, `Staging`
* **Test Scenarios:**
  1. Generate valid access + refresh tokens
  2. Logout and verify tokens are blacklisted
  3. Attempt API calls with blacklisted tokens
  4. Verify 401 response
  5. Wait for TTL expiry and confirm Redis cleanup
* **Performance Test:** Validate 1000 tokens/second with blacklist check

---

h2. 📎 Resources & Attachments
* **Related Tickets:** Part of SLO Epic
* **Documentation:** [JWT Best Practices - Token Revocation](https://tools.ietf.org/html/rfc7519)

---

### TASK 4: Session & Logout Table Validation
**Estimate:** 1 Day

h2. 📖 User Story / Context
* **As a:** Backend Developer
* **I want to:** Validate session table and logout table entries
* **So that:** Data integrity is maintained and logout events are properly tracked for auditing

---

h2. ✅ Acceptance Criteria (Definition of Done)

* [ ] **Scenario 1:** Session table updated on logout
   * Given User has active session in `sessions` table
   * When User logs out
   * Then Session status is updated to 'LOGGED_OUT' with logout_timestamp
* [ ] **Scenario 2:** Logout event recorded
   * Given User initiates logout
   * When Logout is processed
   * Then Entry is created in `logout_events` table with user_id, session_id, logout_type, timestamp
* [ ] **Scenario 3:** Orphaned session cleanup
   * Given Sessions exist beyond token expiry
   * When Daily cleanup job runs
   * Then Expired sessions are marked as 'EXPIRED' in sessions table
* [ ] **Data Validation:** 
  - All logout events have corresponding session entries
  - No active sessions for logged-out users
  - Logout timestamps are consistent across tables
* [ ] **Reporting:** Admin dashboard shows logout statistics

---

h2. 🛠 Technical Implementation Notes
* **Database Changes:**
  ```sql
  -- sessions table update
  ALTER TABLE sessions ADD COLUMN logout_timestamp TIMESTAMP NULL;
  ALTER TABLE sessions ADD COLUMN status VARCHAR(20) DEFAULT 'ACTIVE';
  CREATE INDEX idx_sessions_status ON sessions(status);
  
  -- logout_events table creation
  CREATE TABLE logout_events (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    session_id UUID NOT NULL,
    logout_type VARCHAR(50) NOT NULL, -- 'SP_LOGOUT', 'IDP_LOGOUT', 'ADMIN_FORCED'
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (session_id) REFERENCES sessions(id)
  );
  CREATE INDEX idx_logout_events_user ON logout_events(user_id);
  CREATE INDEX idx_logout_events_timestamp ON logout_events(created_at);
  ```
* **APIs:**
  - `GET /api/v1/admin/logout-events` - Fetch logout audit logs
  - `GET /api/v1/admin/sessions?status=LOGGED_OUT` - Query logged out sessions
* **Background Jobs:**
  - `SessionCleanupJob` - Runs daily at 2 AM UTC

---

h2. 🧪 QA & Test Data
* **Test Environment:** `Staging`
* **Test Scenarios:**
  1. Perform various logout types (SP, IDP, Admin-forced)
  2. Verify all create corresponding logout_events entries
  3. Check session table status updates
  4. Run cleanup job and verify expired session handling
  5. Test admin dashboard logout reports
* **Data Validation:**
  - Run SQL queries to verify referential integrity
  - Check for orphaned records

---

h2. 📎 Resources & Attachments
* **Migration Script:** `migrations/2024_02_add_logout_tables.sql`
* **Related Tickets:** Final task in SLO Epic

---

## Epic Summary
This epic delivers comprehensive Single Logout functionality with proper token management, session tracking, and audit logging. All tasks are interconnected and should be completed sequentially for smooth integration.
