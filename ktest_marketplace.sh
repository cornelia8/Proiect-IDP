#!/bin/bash

# Exit if any command fails
set -e

GATEWAY_URL="http://marketplace.local"

echo "🚀 Starting marketplace test!"

# Seller signup and login
echo "🔵 Signing up seller_user..."
curl -s -X POST $GATEWAY_URL/signup -H "Content-Type: application/json" -d '{"username":"seller_user","password":"password"}'

echo "🔵 Logging in seller_user..."
SELLER_TOKEN=$(curl -s -X POST $GATEWAY_URL/login -H "Content-Type: application/json" -d '{"username":"seller_user","password":"password"}' | jq -r '.token')
echo "Seller Token: $SELLER_TOKEN"

# Buyer signup and login
echo "🟢 Signing up buyer_user..."
curl -s -X POST $GATEWAY_URL/signup -H "Content-Type: application/json" -d '{"username":"buyer_user","password":"password"}'

echo "🟢 Logging in buyer_user..."
BUYER_TOKEN=$(curl -s -X POST $GATEWAY_URL/login -H "Content-Type: application/json" -d '{"username":"buyer_user","password":"password"}' | jq -r '.token')
echo "Buyer Token: $BUYER_TOKEN"

# Seller posts two items
echo "🔵 Seller posts item 1..."
curl -s -X POST $GATEWAY_URL/items \
  -H "Authorization: Bearer $SELLER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Gaming Laptop","description":"High-end laptop","price":2500}'

echo "🔵 Seller posts item 2..."
curl -s -X POST $GATEWAY_URL/items \
  -H "Authorization: Bearer $SELLER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Gaming Laptop","description":"High-end laptop","price":2500}'

# Check items
echo "🛒 Current items for sale:"
curl -s $GATEWAY_URL/items | jq

# Buyer buys item 1
echo "🟢 Buyer buys item 1..."
curl -s -X POST $GATEWAY_URL/transactions \
  -H "Authorization: Bearer $BUYER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"item_id":1}'

# Check items after purchase
echo "🛒 Items after purchase:"
curl -s $GATEWAY_URL/items | jq

# Buyer views their transactions
echo "🟢 Buyer checking their transactions..."
curl -s -H "Authorization: Bearer $BUYER_TOKEN" $GATEWAY_URL/transactions | jq

# Seller tries to view transactions (should be empty for now)
echo "🔵 Seller checking their transactions (should be empty as buyer-only view for now)..."
curl -s -H "Authorization: Bearer $SELLER_TOKEN" $GATEWAY_URL/transactions | jq

echo "✅ Test finished successfully!"
