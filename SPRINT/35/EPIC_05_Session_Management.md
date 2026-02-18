# EPIC: Session Management

**Epic Duration:** 3 Days  
**Sprint:** SPRINT 35  
**Priority:** High

---

## Epic Description
Implement comprehensive session tracking and management system that monitors user devices, provides session visibility, and enables administrators to remotely logout users from specific devices for both SAML and Token-based authentication.

---

## TASK 1: Device Tracking on Login (SAML + Token)
**Estimate:** 1 Day (Frontend: 4hrs + Backend: 4hrs)

h2. 📖 User Story / Context
* **As a:** Security Administrator
* **I want to:** Track device information when users login
* **So that:** I can monitor user sessions and detect suspicious login patterns

---

h2. ✅ Acceptance Criteria (Definition of Done)

* [ ] **Scenario 1:** Device info captured on login
   * Given User logs in via SAML or Token
   * When Authentication succeeds
   * Then Device info (IP, Browser, OS, Device Type) is recorded
* [ ] **Scenario 2:** Multiple devices tracked
   * Given User logs in from different devices
   * When Each login occurs
   * Then Separate session entries created for each device
* [ ] **Data Captured:**
   * IP Address
   * Browser (name and version)
   * Operating System
   * Device Type (Mobile, Desktop, Tablet)
   * Location (city, country) - if available
   * Login timestamp

---

h2. 🛠 Technical Implementation Notes
* **Database Schema:**
  ```sql
  CREATE TABLE user_sessions (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    session_token VARCHAR(255) UNIQUE NOT NULL,
    ip_address VARCHAR(45),
    user_agent TEXT,
    browser VARCHAR(100),
    os VARCHAR(100),
    device_type VARCHAR(20), -- 'mobile', 'desktop', 'tablet'
    location_city VARCHAR(100),
    location_country VARCHAR(100),
    auth_type VARCHAR(20), -- 'SAML', 'TOKEN'
    is_active BOOLEAN DEFAULT true,
    last_activity TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP
  );
  CREATE INDEX idx_user_sessions_user_id ON user_sessions(user_id);
  CREATE INDEX idx_user_sessions_active ON user_sessions(is_active);
  ```
* **Backend:**
  - Parse User-Agent header using `ua-parser-js`
  - Get IP from request headers (X-Forwarded-For, X-Real-IP)
  - Use GeoIP library for location detection
* **Frontend:**
  - Send User-Agent automatically in headers
  - No additional frontend work needed

---

h2. 🧪 QA & Test Data
* **Test Environment:** Development, Staging
* **Tests:**
  - Login from Chrome on Windows
  - Login from Safari on iPhone
  - Verify session table has correct device info
  - Check IP address accuracy
  - Validate browser and OS detection

---

h2. 📎 Resources & Attachments
* **Libraries:** `ua-parser-js`, `geoip-lite`

---

## TASK 2: User Session List Display
**Estimate:** 1 Day (Frontend: 4hrs + Backend: 4hrs)

h2. 📖 User Story / Context
* **As a:** User
* **I want to:** View all my active sessions
* **So that:** I can see where I'm logged in and manage my account security

---

h2. ✅ Acceptance Criteria (Definition of Done)

* [ ] **Scenario 1:** User views their session list
   * Given User is authenticated
   * When User navigates to "Active Sessions" page
   * Then All active sessions are displayed with device details
* [ ] **Scenario 2:** Session details shown
   * Given Sessions exist
   * When List is rendered
   * Then Each session shows: Device, Browser, OS, Location, Last Activity, Login Time
* [ ] **Scenario 3:** Current session highlighted
   * Given User viewing session list
   * When List is displayed
   * Then Current session is marked as "This Device"
* [ ] **UI/UX:** Clean card-based layout with icons for device types

---

h2. 🛠 Technical Implementation Notes
* **API Endpoint:** `GET /api/v1/users/sessions`
* **Response:**
  ```json
  {
    "sessions": [
      {
        "id": "uuid",
        "browser": "Chrome 120",
        "os": "Windows 10",
        "deviceType": "desktop",
        "location": "Kathmandu, Nepal",
        "ipAddress": "103.10.29.xxx",
        "lastActivity": "2024-02-13T10:00:00Z",
        "createdAt": "2024-02-10T08:30:00Z",
        "isCurrent": true
      }
    ]
  }
  ```
* **Frontend Component:** `ActiveSessionsList.tsx`
* **Icons:** Use device icons (desktop, mobile, tablet)

---

h2. 🧪 QA & Test Data
* **Tests:**
  - Create multiple sessions from different devices
  - Verify all sessions appear in list
  - Check current device highlighting
  - Test responsive design on mobile

---

## TASK 3: Admin Logout from Selective Devices
**Estimate:** 1 Day (Frontend: 4hrs + Backend: 4hrs)

h2. 📖 User Story / Context
* **As a:** System Administrator
* **I want to:** Force logout users from specific devices
* **So that:** I can terminate suspicious or unauthorized sessions

---

h2. ✅ Acceptance Criteria (Definition of Done)

* [ ] **Scenario 1:** Admin views user's sessions
   * Given Admin is on user management page
   * When Admin clicks "View Sessions" for a user
   * Then All user's active sessions displayed
* [ ] **Scenario 2:** Admin terminates specific session
   * Given Admin viewing user sessions
   * When Admin clicks "Logout" on a session
   * Then Session is terminated and tokens/SAML revoked
* [ ] **Scenario 3:** User receives notification
   * Given Admin logs out user's session
   * When Session is terminated
   * Then User sees "Session expired" message and is logged out
* [ ] **Audit:** All admin logouts logged for security audit

---

h2. 🛠 Technical Implementation Notes
* **API Endpoints:**
  - `GET /api/v1/admin/users/:userId/sessions` - View user sessions
  - `DELETE /api/v1/admin/sessions/:sessionId` - Terminate session
* **Backend Logic:**
  - Mark session as inactive
  - Add token to blacklist
  - Invalidate SAML assertion
  - Create audit log entry
* **Frontend:**
  - Admin dashboard with user session management
  - Confirmation modal before logout
  - Bulk logout option (logout all sessions)

---

h2. 🧪 QA & Test Data
* **Test Environment:** Staging
* **Tests:**
  - Admin views user sessions
  - Admin terminates one session
  - Verify user is immediately logged out on that device
  - Check audit logs
  - Test bulk logout functionality

---

h2. 📎 Resources & Attachments
* **Security:** Ensure only admins with `MANAGE_SESSIONS` permission can access
