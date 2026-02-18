# EPIC: Implement PROTO Auto Generated Import

**Epic Duration:** 2.5 Days  
**Sprint:** SPRINT 35  
**Priority:** High

---

## Epic Description
Migrate all microservices from manual gRPC client configuration to auto-generated TypeScript definitions from the centralized `vle-proto` package for type safety and consistency.

---

## Tasks

### TASK 1: VLE-Account Service Proto Integration
**Estimate:** 1 Day

h2. 📖 User Story / Context
* **As a:** Backend Developer
* **I want to:** Replace manual gRPC client configurations in VLE-Account with auto-generated imports
* **So that:** Proto definitions are centralized and type-safe

---

h2. ✅ Acceptance Criteria (Definition of Done)

* [ ] **Scenario 1:** Remove manual proto definitions and use `vle-proto` package
* [ ] **Scenario 2:** All imports use `vle-proto/dist/vle/account/v1/*` paths
* [ ] **Scenario 3:** TypeScript compiles without type errors
* [ ] **Scenario 4:** All gRPC calls functional with proper request/response types
* [ ] **Code Quality:** No hardcoded proto paths

---

h2. 🛠 Technical Implementation Notes
* **Package:** `npm install vle-proto@latest`
* **Files to Update:**
  - `src/grpc/grpc-clients.config.ts`
  - `src/modules/account/account.service.ts`
  - `src/modules/auth/auth.service.ts`
* **Remove:** `src/proto/` directory

---

h2. 🧪 QA & Test Data
* **Test Environment:** Development, Staging
* **Tests:** Integration tests, `npm run build`, `npm run test:e2e`

---

### TASK 2: IDP Service Proto Integration
**Estimate:** 4 Hours

h2. 📖 User Story / Context
* **As a:** Backend Developer
* **I want to:** Migrate IDP service to auto-generated proto imports
* **So that:** IDP maintains type safety

---

h2. ✅ Acceptance Criteria (Definition of Done)

* [ ] Manual proto files removed
* [ ] gRPC server definitions use auto-generated code
* [ ] SAML and OAuth services functional
* [ ] Build and deploy successful

---

h2. 🛠 Technical Implementation Notes
* **Files:** `grpc.config.ts`, `saml.service.ts`, `oauth.service.ts`
* **Import:** `vle-proto/dist/vle/identity/v1/*`

---

h2. 🧪 QA & Test Data
* **Tests:** OAuth flow, SAML SSO, `npm run test:e2e`

---

### TASK 3: Super Admin Service Proto Integration
**Estimate:** 4 Hours

h2. 📖 User Story / Context
* **As a:** Backend Developer
* **I want to:** Refactor Super Admin to use auto-generated proto imports
* **So that:** Admin operations maintain type safety

---

h2. ✅ Acceptance Criteria (Definition of Done)

* [ ] Manual proto definitions removed
* [ ] Admin gRPC APIs use auto-generated types
* [ ] All admin operations functional
* [ ] Integration tests pass

---

h2. 🛠 Technical Implementation Notes
* **Files:** `users.service.ts`, `tenants.service.ts`, `sp.service.ts`
* **Import:** `vle-proto/dist/vle/admin/v1/*`

---

h2. 🧪 QA & Test Data
* **Tests:** Create user, delete SP, audit logs

---

### TASK 4: MyKademy-API Service Proto Integration
**Estimate:** 4 Hours

h2. 📖 User Story / Context
* **As a:** Backend Developer
* **I want to:** Update MyKademy-API to use auto-generated proto imports
* **So that:** Type safety is maintained with VLE microservices

---

h2. ✅ Acceptance Criteria (Definition of Done)

* [ ] Manual proto files removed
* [ ] gRPC client calls to IDP updated
* [ ] User authentication flow works
* [ ] All REST APIs functional

---

h2. 🛠 Technical Implementation Notes
* **Files:** `auth.middleware.ts`, `users.service.ts`
* **Import:** `vle-proto/dist/vle/identity/v1/*`

---

h2. 🧪 QA & Test Data
* **Tests:** Login flow, token validation, course APIs, load testing

---

## Epic Summary
Migrates all four microservices to use centralized `vle-proto` package for type safety and consistency.
