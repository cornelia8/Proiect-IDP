# CHANGELOG

## [April 23, 2025]

- Started a simple client server application using JavaScript and Nodejs supporting multiple clients
- Added a basic Docker compose configuration for it

## [April 24, 2025]

- Created 2 versions for a database configuration using PostgreSQL
- Added a js server for said database

## [April 25, 2025]
- Dropped JavaScript in favor of Python
- Built user_service:
  - User signup with password hashing.
  - User login with JWT token generation.
  - Endpoints for fetching users by ID and username without exposing passwords.
- Built shop_service:
  - Allow sellers to list items (POST /items).
  - Allow public listing of items (GET /items).
- Dockerized user_service and shop_service.

- Built transaction_service:
  - Buyer can purchase items.
  - Items are fetched from shop_service at purchase time.
  - After buying, the item is deleted.
  - Each transaction records buyer, seller, item name, and price.
- Connected all services via an api_gateway.
- Set up Prometheus metrics for all Flask apps.
- Full docker-compose orchestration for all services.

## [April 26, 2025]

- Implemented JWT authentication throughout api_gateway.
  - Only logged-in sellers can POST items.
  - Only logged-in buyers can POST transactions.
  - Only logged-in buyers can view their transactions.
- Made marketplace browsing public (GET /items does not require login).
- Protected sensitive routes with token checks.
- Introduced uniform error handling (404, 500, JWT errors).
- Added secret key environment consistency across services.

## [April 27, 2025]
- Wrote and tested a full marketplace bash script:
  - Seller signs up, logs in, lists items.
  - Buyer signs up, logs in, buys an item.
  - Buyer views his transactions, seller sees empty (as expected).
- Validated complete purchase flow.
- Ensured token expiration works correctly.
- Validated Prometheus `/metrics` endpoints.
- Prepared system for future extensions (pagination, seller sales view).

# CONTRIBUTIONS
DUTULESCU ALEXANDRU api_gateway, transaction_service, user service, testing, yaml config files
MARCULESCU GABRIELA CORNELIA monitoring, shop service, README, CHANGELOG, Docker Compose 

