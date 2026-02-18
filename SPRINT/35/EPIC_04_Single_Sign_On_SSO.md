# EPIC: Single Sign On (SSO)

**Epic Duration:** 5 Days  
**Sprint:** SPRINT 35  
**Priority:** High

---

## Epic Description
Implement comprehensive Single Sign-On functionality enabling seamless product switching between MyKademy and VLE Admin using SAML-to-Token conversion and bidirectional SSO flows.

---

## TASK 1: Understand SSO Flow Architecture
**Estimate:** 1 Day

h2. 📖 User Story / Context
* **As a:** Development Team
* **I want to:** Thoroughly understand SAML SSO and OAuth 2.0 integration flows
* **So that:** Implementation follows security best practices and industry standards

---

h2. ✅ Acceptance Criteria (Definition of Done)

* [ ] **Architecture Documentation:** Complete flow diagrams created for SAML and OAuth flows
* [ ] **Security Review:** Security implications documented and mitigation strategies identified
* [ ] **Technical Spike:** POC created demonstrating SAML assertion to JWT token exchange
* [ ] **Team Knowledge:** Knowledge sharing session completed with development team

---

h2. 🛠 Technical Implementation Notes
* **Research Areas:**
  - SAML 2.0 Web Browser SSO Profile
  - OAuth 2.0 Token Exchange (RFC 8693)
  - SAML assertion validation and signature verification
  - Session management across applications
* **Deliverables:**
  - Sequence diagrams (use Mermaid or PlantUML)
  - Security threat model document
  - POC code demonstrating SAML-to-JWT conversion

---

h2. 📎 Resources & Attachments
* **SAML Spec:** [SAML 2.0 Technical Overview](http://docs.oasis-open.org/security/saml/Post2.0/sstc-saml-tech-overview-2.0.html)
* **OAuth Token Exchange:** [RFC 8693](https://datatracker.ietf.org/doc/html/rfc8693)

---

## TASK 2: Product Switch Auto Login - SAML to Token
**Estimate:** 1 Day

h2. 📖 User Story / Context
* **As a:** User authenticated via SAML
* **I want to:** Automatically receive a JWT token when switching products
* **So that:** I don't need to re-authenticate when moving between MyKademy and VLE

---

h2. ✅ Acceptance Criteria (Definition of Done)

* [ ] **Scenario 1:** SAML assertion to JWT conversion
   * Given User authenticated via SAML
   * When Product switch is initiated
   * Then Valid JWT access token is generated from SAML assertion
* [ ] **Scenario 2:** Token contains correct user claims
   * Given SAML assertion has user attributes
   * When Token is generated
   * Then JWT contains userId, email, roles from SAML assertion
* [ ] **Security:** 
   * SAML signature validated before token issuance
   * Token expiry matches session policy
   * Audit log created for token generation

---

h2. 🛠 Technical Implementation Notes
* **API Endpoint:** `POST /api/v1/auth/saml-to-token`
* **Request:**
  ```json
  {
    "samlAssertion": "<base64-encoded-assertion>",
    "targetService": "vle-admin"
  }
  ```
* **Response:**
  ```json
  {
    "accessToken": "eyJhbGc...",
    "refreshToken": "eyJhbGc...",
    "expiresIn": 900
  }
  ```
* **Components:**
  - `SAMLTokenConverter.convertToJWT(assertion)`
  - `SAMLValidator.validateAssertion(assertion)`

---

h2. 🧪 QA & Test Data
* **Test Environment:** Staging
* **Tests:** SAML assertion validation, token generation, claim mapping

---

## TASK 3: MyKademy SAML to Token Implementation
**Estimate:** 1 Day

h2. 📖 User Story / Context
* **As a:** MyKademy User
* **I want to:** Switch to VLE Admin with automatic authentication
* **So that:** My workflow is seamless without re-entering credentials

---

h2. ✅ Acceptance Criteria (Definition of Done)

* [ ] MyKademy frontend triggers SAML-to-token API
* [ ] Received JWT token stored securely
* [ ] User redirected to VLE Admin with valid session
* [ ] Session persists across tab refreshes

---

h2. 🛠 Technical Implementation Notes
* **Frontend Changes:**
  - `ProductSwitcher.tsx` component
  - Call `/api/v1/auth/saml-to-token` endpoint
  - Store tokens in httpOnly cookies or sessionStorage
  - Redirect to VLE Admin with token

---

h2. 🧪 QA & Test Data
* **Tests:** End-to-end product switch, token validation, error handling

---

## TASK 4: VLE Admin to MyKademy SSO
**Estimate:** 1 Day

h2. 📖 User Story / Context
* **As a:** VLE Admin User
* **I want to:** Switch to MyKademy with automatic authentication
* **So that:** I can seamlessly access both platforms

---

h2. ✅ Acceptance Criteria (Definition of Done)

* [ ] VLE Admin triggers SSO to MyKademy
* [ ] SAML assertion or JWT token used for authentication
* [ ] User lands on MyKademy dashboard authenticated
* [ ] Works bidirectionally with Task 3

---

h2. 🛠 Technical Implementation Notes
* **API:** `POST /api/v1/auth/initiate-sso`
* **Frontend:** Update VLE Admin navigation with product switcher

---

h2. 🧪 QA & Test Data
* **Tests:** Bidirectional SSO, session synchronization, logout propagation

---

## TASK 5: MyKademy to VLE Admin SSO
**Estimate:** 1 Day

h2. 📖 User Story / Context
* **As a:** MyKademy User with VLE permissions
* **I want to:** Access VLE Admin directly from MyKademy
* **So that:** I can manage VLE content efficiently

---

h2. ✅ Acceptance Criteria (Definition of Done)

* [ ] MyKademy frontend initiates SSO to VLE Admin
* [ ] User automatically authenticated on VLE Admin
* [ ] Role-based access enforced (only users with VLE roles can access)
* [ ] Performance: SSO completes within < 2 seconds

---

h2. 🛠 Technical Implementation Notes
* **Components:**
  - Update MyKademy navigation menu
  - Role validation before SSO initiation
  - Token exchange API integration

---

h2. 🧪 QA & Test Data
* **Tests:** Role-based access, error handling for unauthorized users, performance testing
