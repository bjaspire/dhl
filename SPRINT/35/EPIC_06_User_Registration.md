# EPIC: User Registration

**Epic Duration:** 5 Days  
**Sprint:** SPRINT 35  
**Priority:** High

---

## Epic Description
Implement complete user registration and profile management system including IDP registration with SP synchronization, email verification, password management, and user profile functionality.

---

## TASK 1: User Registration in IDP with SP Sync
**Estimate:** 1 Day (Frontend: 4hrs + Backend: 4hrs)

h2. 📖 User Story / Context
* **As a:** New User
* **I want to:** Register an account in the Identity Provider
* **So that:** I can access MyKademy and VLE services with Single Sign-On

---

h2. ✅ Acceptance Criteria (Definition of Done)

* [ ] **Scenario 1:** User completes registration form
   * Given User accesses registration page
   * When User fills email, name, and other details
   * Then Account is created in IDP
* [ ] **Scenario 2:** Account synchronized to SP (MyKademy)
   * Given User registered in IDP
   * When Registration is successful
   * Then User account is created in MyKademy database
* [ ] **Scenario 3:** Validation enforced
   * Given User submits registration
   * When Data is invalid (duplicate email, weak password)
   * Then Error messages displayed
* [ ] **UI/UX:** Modern registration form with real-time validation

---

h2. 🛠 Technical Implementation Notes
* **API Endpoint:** `POST /api/v1/auth/register`
* **Request:**
  ```json
  {
    "email": "user@example.com",
    "firstName": "John",
    "lastName": "Doe",
    "password": "SecurePass123!",
    "acceptTerms": true
  }
  ```
* **Backend:**
  - Create user in IDP database
  - Hash password with bcrypt
  - Trigger gRPC call to MyKademy to sync user
  - Send verification email
* **Frontend:** `RegisterForm.tsx` with client-side validation

---

h2. 🧪 QA & Test Data
* **Tests:**
  - Valid registration
  - Duplicate email rejection
  - Weak password rejection
  - Verify account created in both IDP and MyKademy

---

## TASK 2: Email Verification
**Estimate:** 1 Day (Frontend: 4hrs + Backend: 4hrs)

h2. 📖 User Story / Context
* **As a:** New User
* **I want to:** Receive email verification after registration
* **So that:** My email ownership is confirmed

---

h2. ✅ Acceptance Criteria (Definition of Done)

* [ ] **Scenario 1:** Verification email sent
   * Given User completes registration
   * When Account is created
   * Then Verification email sent to user's email
* [ ] **Scenario 2:** User verifies email
   * Given User receives verification email
   * When User clicks verification link
   * Then Account is marked as verified
* [ ] **Scenario 3:** Token expiry
   * Given Verification link is > 24 hours old
   * When User clicks expired link
   * Then Error shown with option to resend
* [ ] **Email Template:** Professional HTML email with branding

---

h2. 🛠 Technical Implementation Notes
* **Database:**
  ```sql
  ALTER TABLE users ADD COLUMN email_verified BOOLEAN DEFAULT false;
  ALTER TABLE users ADD COLUMN verification_token VARCHAR(255);
  ALTER TABLE users ADD COLUMN verification_expires_at TIMESTAMP;
  ```
* **API Endpoints:**
  - `POST /api/v1/auth/verify-email?token=xxx`
  - `POST /api/v1/auth/resend-verification`
* **Email Service:**
  - Use SendGrid or AWS SES
  - Template with verification link
  - Token valid for 24 hours

---

h2. 🧪 QA & Test Data
* **Tests:**
  - Register and verify email
  - Test expired token
  - Test resend verification
  - Check email delivery

---

## TASK 3: Password Setup with Validation
**Estimate:** 4 Hours

h2. 📖 User Story / Context
* **As a:** User
* **I want to:** Set a strong password during registration
* **So that:** My account is secure

---

h2. ✅ Acceptance Criteria (Definition of Done)

* [ ] **Password Requirements:**
   * Minimum 8 characters
   * At least 1 uppercase letter
   * At least 1 number
   * At least 1 special character
* [ ] **Real-time validation:** Password strength indicator
* [ ] **Confirmation:** Password confirmation field must match
* [ ] **Security:** Password hashed with bcrypt (12 rounds)

---

h2. 🛠 Technical Implementation Notes
* **Frontend:** Password strength indicator component
* **Validation Library:** `zod` or `yup`
* **Backend:** bcrypt hashing before storage

---

h2. 🧪 QA & Test Data
* **Tests:** Weak password rejection, strong password acceptance, mismatch handling

---

## TASK 4: Forgot Password & Reset
**Estimate:** 1 Day (Frontend: 4hrs + Backend: 4hrs)

h2. 📖 User Story / Context
* **As a:** User who forgot password
* **I want to:** Reset my password via email link
* **So that:** I can regain access to my account

---

h2. ✅ Acceptance Criteria (Definition of Done)

* [ ] **Scenario 1:** User requests password reset
   * Given User clicks "Forgot Password"
   * When User enters email
   * Then Reset link sent to email
* [ ] **Scenario 2:** User resets password
   * Given User receives reset email
   * When User clicks link and sets new password
   * Then Password updated successfully
* [ ] **Security:**
   * Reset token valid for 1 hour
   * Token single-use only
   * Old sessions invalidated after reset

---

h2. 🛠 Technical Implementation Notes
* **API Endpoints:**
  - `POST /api/v1/auth/forgot-password`
  - `POST /api/v1/auth/reset-password`
* **Database:**
  ```sql
  CREATE TABLE password_reset_tokens (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    token VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    used BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT NOW()
  );
  ```

---

h2. 🧪 QA & Test Data
* **Tests:** Request reset, verify email, reset password, test token expiry

---

## TASK 5: User Profile Page
**Estimate:** 4 Hours (Frontend: 2hrs + Backend: 2hrs)

h2. 📖 User Story / Context
* **As a:** User
* **I want to:** View my profile information
* **So that:** I can see my account details

---

h2. ✅ Acceptance Criteria (Definition of Done)

* [ ] Profile page displays: Name, Email, Role, Join Date
* [ ] Avatar/Profile Picture support
* [ ] Responsive design

---

h2. 🛠 Technical Implementation Notes
* **API:** `GET /api/v1/users/me`
* **Component:** `UserProfile.tsx`

---

## TASK 6: User Profile Edit (Including Password Change)
**Estimate:** 1 Day (Frontend: 4hrs + Backend: 4hrs)

h2. 📖 User Story / Context
* **As a:** User
* **I want to:** Edit my profile and change password
* **So that:** I can keep my information up-to-date

---

h2. ✅ Acceptance Criteria (Definition of Done)

* [ ] User can update name, email
* [ ] Email change requires verification
* [ ] Password change requires current password
* [ ] Real-time validation

---

h2. 🛠 Technical Implementation Notes
* **API Endpoints:**
  - `PATCH /api/v1/users/me`
  - `POST /api/v1/users/change-password`

---

h2. 🧪 QA & Test Data
* **Tests:** Update profile, change email, change password, validation
