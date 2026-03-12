1. Mykademy LMS - set which IDP use OLD or NEW ( Superadmin - (accounts) setting)
    - Conditional Change SAML FLOW ( all SP)
    - OLD API token verification - conditional for NEW IDP token and OLD IDP token

2. Student Dashboard
    - Refresh Token implement ( Interceptor ) for new IDP

3. OLD IDP functionality migrate:
    - NEW IDP : User Management finalyze
    - SP Update 
    - LTI 
    - Password Update 
    - Subscribtion ( charge bee )
    ( - Onboarding - )

4. Generate Auth Token:
    - Create functionality for generate auth token API Gateway ( VLE -admin )

5. Setting 
  - Global Setting - VLE ADMIN ( flag )



Tasks:

EPIC - Conditional change OLD VS NEW IDP
- Conditional Change SAML FLOW ( LMS ) - 1.5 Days - Rakesh
- OLD API token verification - conditional for NEW IDP token and OLD IDP token - 1.5 Days - Rakesh

EPIC - Student Dashboard
- Refresh Token implement ( Interceptor ) for new IDP - 1.5 Day : Bhasker 

EPIC - OLD IDP functionality migrate:
- NEW IDP : User Management finalyze ( LMS, TMS, Student Dashboard) : 2 Days : Rakesh - check and fix 
- SP Update : 1 Day : Rakesh X
- LTI : 1 Day : Rakesh X 
- Subscribtion ( charge bee ) : X
( - Onboarding - ) X

EPIC - Generate Auth Token:
- Create functionality for generate auth token API Gateway ( VLE -admin ) : 
    SUB: 
        - Generate auth token ( Completely Fresh rewrite on API - gateway (VLE-admin)) - 3d
        - Implement on respective SPS ( MYkademy, StudentDashbord,DMS, TMS, E-portfolio) -  1d
        - Write New API for other data like ( get allow products, analytics, s3 urls, tilezone, etc ) - 1d
        -



EPIC - Setting 
- Global Setting - VLE ADMIN ( flag )

