# EPIC: IDP Seed Configuration with Default Values

**Epic Duration:** 2 Days  
**Sprint:** SPRINT 35  
**Priority:** High  
**Epic Owner:** [Assign to DevOps/Backend Lead]  
**Related Ticket:** MYK-2598

---

## Epic Description
Set up Identity Provider (IDP) with default configuration including RSA key pair generation, default tenant settings, OAuth client configurations, and essential bootstrap data required for IDP to function in development, staging, and production environments.

---

## Tasks

### TASK 1: RSA Key Pair Generation & Storage
**Estimate:** 4 Hours

h2. 📖 User Story / Context
* **As a:** DevOps Engineer
* **I want to:** Generate and securely store RSA public/private key pairs for IDP
* **So that:** IDP can sign SAML assertions and JWT tokens cryptographically

---

h2. ✅ Acceptance Criteria (Definition of Done)

* [ ] **Scenario 1:** Automatic RSA key generation on first startup
   * Given IDP starts for the first time without existing keys
   * When Seed script executes
   * Then 2048-bit RSA key pair is generated and stored securely
* [ ] **Scenario 2:** Key persistence
   * Given RSA keys are generated
   * When Keys are stored
   * Then Private key is encrypted and stored in database, public key stored in plain format
* [ ] **Scenario 3:** Key rotation readiness
   * Given System has active keys
   * When New keys are generated
   * Then Both old and new keys are maintained (with validity period)
* [ ] **Security:** 
   * Private key never exposed in logs
   * Keys stored with AES-256 encryption
   * Only IDP service has decrypt permission
* [ ] **Validation:** Keys can successfully sign and verify JWT tokens

---

h2. 🛠 Technical Implementation Notes
* **Database Schema:**
  ```sql
  CREATE TABLE idp_keys (
    id UUID PRIMARY KEY,
    key_id VARCHAR(50) UNIQUE NOT NULL, -- Used in JWT header "kid"
    public_key TEXT NOT NULL,
    private_key_encrypted TEXT NOT NULL,
    algorithm VARCHAR(20) DEFAULT 'RS256',
    is_active BOOLEAN DEFAULT true,
    valid_from TIMESTAMP DEFAULT NOW(),
    valid_until TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
  );
  CREATE INDEX idx_idp_keys_active ON idp_keys(is_active);
  ```
* **Key Generation:**
  - Use Node.js `crypto` module or library like `node-forge`
  - Algorithm: RSA
  - Key size: 2048 bits
  - Format: PEM
* **Encryption:**
  - Private key encrypted using AES-256-GCM
  - Encryption key stored in environment variable `IDP_KEY_ENCRYPTION_SECRET`
* **Components:**
  - `KeyGenerationService.generateRSAKeyPair()`
  - `KeyStorageService.storeKeys(publicKey, privateKey)`
  - `KeyManagementService.getActiveKey()`
* **Seed Script:** `scripts/seed-idp-keys.ts`

---

h2. 🧪 QA & Test Data
* **Test Environment:** `Development`, `Staging`
* **Test Scenarios:**
  1. Run seed script on fresh database
  2. Verify keys are generated and stored
  3. Sign a JWT token using private key
  4. Verify JWT token using public key
  5. Check private key is encrypted in database
  6. Attempt to generate keys again (should skip if exists)
* **Security Test:** 
  - Verify private key cannot be extracted from logs
  - Confirm encryption/decryption works correctly

---

h2. 📎 Resources & Attachments
* **Related Tickets:** MYK-2598
* **Documentation:** [RSA Key Generation Best Practices](https://www.rfc-editor.org/rfc/rfc8017)
* **Libraries:** `node-forge`, `jsonwebtoken`, `crypto`

---

### TASK 2: Default IDP Configuration & Settings
**Estimate:** 4 Hours

h2. 📖 User Story / Context
* **As a:** System Administrator
* **I want to:** Bootstrap IDP with default configuration values
* **So that:** IDP can operate with sensible defaults in all environments without manual setup

---

h2. ✅ Acceptance Criteria (Definition of Done)

* [ ] **Scenario 1:** Default settings seeded on initialization
   * Given IDP database is empty
   * When Seed script runs
   * Then Default configurations are created (session timeout, token expiry, etc.)
* [ ] **Scenario 2:** Environment-specific overrides
   * Given Environment variables are set
   * When IDP starts
   * Then Environment values override default seed values
* [ ] **Scenario 3:** Settings validation
   * Given Seed data is applied
   * When IDP validates configuration
   * Then All required settings are present and valid
* [ ] **Configuration includes:**
   * Session timeout: 30 minutes
   * Access token expiry: 15 minutes
   * Refresh token expiry: 7 days
   * SAML assertion expiry: 5 minutes
   * Max concurrent sessions per user: 5
   * Password policy settings
   * Default theme settings

---

h2. 🛠 Technical Implementation Notes
* **Database Schema:**
  ```sql
  CREATE TABLE idp_config (
    id UUID PRIMARY KEY,
    config_key VARCHAR(100) UNIQUE NOT NULL,
    config_value TEXT NOT NULL,
    data_type VARCHAR(20), -- 'string', 'number', 'boolean', 'json'
    description TEXT,
    is_system BOOLEAN DEFAULT false, -- Cannot be deleted by users
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
  );
  ```
* **Seed Data:**
  ```json
  {
    "session_timeout_minutes": 30,
    "access_token_expiry_minutes": 15,
    "refresh_token_expiry_days": 7,
    "saml_assertion_expiry_minutes": 5,
    "max_concurrent_sessions": 5,
    "password_min_length": 8,
    "password_require_uppercase": true,
    "password_require_numbers": true,
    "password_require_special_chars": true,
    "account_lockout_threshold": 5,
    "account_lockout_duration_minutes": 15,
    "idp_entity_id": "https://idp.mykademy.com",
    "idp_sso_url": "https://idp.mykademy.com/saml/sso",
    "idp_slo_url": "https://idp.mykademy.com/saml/slo"
  }
  ```
* **Seed Script:** `scripts/seed-idp-config.ts`
* **Components:**
  - `ConfigService.getSetting(key)`
  - `ConfigService.getSettingWithDefault(key, defaultValue)`

---

h2. 🧪 QA & Test Data
* **Test Environment:** `Development`
* **Test Scenarios:**
  1. Run seed script on empty database
  2. Verify all config entries are created
  3. Update a config value via API
  4. Restart IDP and verify updated value persists
  5. Test environment variable override
  6. Verify system configs cannot be deleted

---

h2. 📎 Resources & Attachments
* **Related Tickets:** MYK-2598
* **Seed Script:** `scripts/seed-idp-config.ts`

---

### TASK 3: Default OAuth Clients & Service Providers
**Estimate:** 4 Hours

h2. 📖 User Story / Context
* **As a:** IDP Administrator
* **I want to:** Pre-configure default OAuth clients and SAML Service Providers
* **So that:** MyKademy and VLE applications can immediately authenticate without manual client registration

---

h2. ✅ Acceptance Criteria (Definition of Done)

* [ ] **Scenario 1:** Default OAuth clients seeded
   * Given IDP seed script runs
   * When OAuth clients table is empty
   * Then Default clients for MyKademy, VLE-Admin, and VLE-Account are created
* [ ] **Scenario 2:** Client credentials validation
   * Given Default OAuth client exists
   * When Application authenticates using client_id and client_secret
   * Then Authentication succeeds and tokens are issued
* [ ] **Scenario 3:** SAML SP metadata seeded
   * Given SAML service providers table is empty
   * When Seed script runs
   * Then Default SP entries for MyKademy and VLE are created with metadata
* [ ] **Data includes:**
   * Client ID, Client Secret
   * Allowed redirect URIs
   * Allowed grant types (authorization_code, refresh_token)
   * Allowed scopes (openid, profile, email)
   * SAML metadata (Entity ID, ACS URL, SLO URL)

---

h2. 🛠 Technical Implementation Notes
* **Database Schema:**
  ```sql
  CREATE TABLE oauth_clients (
    id UUID PRIMARY KEY,
    client_id VARCHAR(100) UNIQUE NOT NULL,
    client_secret_hash VARCHAR(255) NOT NULL,
    client_name VARCHAR(255) NOT NULL,
    redirect_uris TEXT[], -- Array of allowed URIs
    grant_types TEXT[], -- ['authorization_code', 'refresh_token']
    scopes TEXT[], -- ['openid', 'profile', 'email']
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
  );
  
  CREATE TABLE saml_service_providers (
    id UUID PRIMARY KEY,
    entity_id VARCHAR(255) UNIQUE NOT NULL,
    sp_name VARCHAR(255) NOT NULL,
    acs_url TEXT NOT NULL, -- Assertion Consumer Service URL
    slo_url TEXT, -- Single Logout URL
    metadata_xml TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
  );
  ```
* **Seed Data:**
  ```json
  {
    "oauth_clients": [
      {
        "client_id": "mykademy-web",
        "client_secret": "<generated-bcrypt-hash>",
        "client_name": "MyKademy Web Application",
        "redirect_uris": ["https://mykademy.com/auth/callback"],
        "grant_types": ["authorization_code", "refresh_token"],
        "scopes": ["openid", "profile", "email", "roles"]
      },
      {
        "client_id": "vle-admin",
        "client_secret": "<generated-bcrypt-hash>",
        "client_name": "VLE Admin Portal",
        "redirect_uris": ["https://vle-admin.mykademy.com/auth/callback"],
        "grant_types": ["authorization_code", "refresh_token"],
        "scopes": ["openid", "profile", "email", "admin"]
      }
    ],
    "saml_sps": [
      {
        "entity_id": "https://mykademy.com/saml",
        "sp_name": "MyKademy SAML SP",
        "acs_url": "https://mykademy.com/saml/acs",
        "slo_url": "https://mykademy.com/saml/slo"
      }
    ]
  }
  ```
* **Seed Script:** `scripts/seed-oauth-clients.ts`
* **Components:**
  - `OAuthClientService.validateClient(clientId, clientSecret)`
  - `SAMLService.getSPMetadata(entityId)`

---

h2. 🧪 QA & Test Data
* **Test Environment:** `Development`, `Staging`
* **Test Scenarios:**
  1. Run seed script
  2. Verify OAuth clients are created
  3. Test OAuth authorization flow with seeded client
  4. Verify SAML SP metadata is accessible
  5. Test SAML SSO with seeded SP
  6. Attempt authentication with invalid client_id (should fail)

---

h2. 📎 Resources & Attachments
* **Related Tickets:** MYK-2598
* **OAuth Spec:** [OAuth 2.0 RFC 6749](https://tools.ietf.org/html/rfc6749)
* **SAML Metadata:** [SAML 2.0 Metadata Spec](http://docs.oasis-open.org/security/saml/v2.0/)

---

### TASK 4: Default Admin User & Roles
**Estimate:** 4 Hours

h2. 📖 User Story / Context
* **As a:** System Administrator
* **I want to:** Create a default admin user and role structure
* **So that:** System administrators can access IDP immediately after deployment

---

h2. ✅ Acceptance Criteria (Definition of Done)

* [ ] **Scenario 1:** Default admin user created
   * Given IDP is freshly installed
   * When Seed script runs
   * Then Admin user with email `admin@mykademy.com` is created
* [ ] **Scenario 2:** Default roles seeded
   * Given Roles table is empty
   * When Seed script runs
   * Then Roles (SUPER_ADMIN, IDP_ADMIN, USER) are created with permissions
* [ ] **Scenario 3:** Admin login
   * Given Default admin user exists
   * When Admin logs in with default credentials
   * Then Authentication succeeds and admin dashboard is accessible
* [ ] **Security:** 
   * Default password must be changed on first login
   * Default password is strong and randomly generated
   * Password is hashed using bcrypt
* [ ] **Documentation:** Default credentials are documented in deployment guide

---

h2. 🛠 Technical Implementation Notes
* **Database Schema:**
  ```sql
  CREATE TABLE roles (
    id UUID PRIMARY KEY,
    role_name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    permissions JSONB, -- Array of permission strings
    is_system BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT NOW()
  );
  
  CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    is_active BOOLEAN DEFAULT true,
    must_change_password BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT NOW()
  );
  
  CREATE TABLE user_roles (
    user_id UUID REFERENCES users(id),
    role_id UUID REFERENCES roles(id),
    PRIMARY KEY (user_id, role_id)
  );
  ```
* **Seed Data:**
  ```json
  {
    "roles": [
      {
        "role_name": "SUPER_ADMIN",
        "description": "Full system access",
        "permissions": ["*"]
      },
      {
        "role_name": "IDP_ADMIN",
        "description": "IDP management access",
        "permissions": ["manage_users", "manage_clients", "manage_sps", "view_logs"]
      },
      {
        "role_name": "USER",
        "description": "Standard user access",
        "permissions": ["view_profile", "update_profile"]
      }
    ],
    "admin_user": {
      "email": "admin@mykademy.com",
      "password": "<randomly-generated-strong-password>",
      "first_name": "System",
      "last_name": "Administrator",
      "must_change_password": true,
      "roles": ["SUPER_ADMIN"]
    }
  }
  ```
* **Seed Script:** `scripts/seed-admin-user.ts`
* **Security:**
  - Password generated using: `crypto.randomBytes(16).toString('base64')`
  - Hashed using bcrypt with salt rounds: 12
  - Output admin credentials to console during seed (only once)

---

h2. 🧪 QA & Test Data
* **Test Environment:** `Development`
* **Test Scenarios:**
  1. Run seed script
  2. Verify default admin user is created
  3. Login with default credentials
  4. Verify must_change_password flag triggers password reset
  5. Verify admin has correct role and permissions
  6. Test role-based access control

---

h2. 📎 Resources & Attachments
* **Related Tickets:** MYK-2598
* **Security Best Practices:** [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)

---

## Epic Summary
This epic establishes the foundational IDP configuration including cryptographic keys, default settings, OAuth clients, SAML service providers, and admin access. All tasks can be executed in parallel and consolidated into a single seed script for deployment automation.

**Deployment Command:**
```bash
npm run seed:idp -- --environment=production
```
