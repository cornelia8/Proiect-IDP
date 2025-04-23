CREATE TABLE Users (
  id SERIAL PRIMARY KEY,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE Products (
  id SERIAL PRIMARY KEY,
  seller_name TEXT NOT NULL,
  product_name TEXT NOT NULL,
  available_quantity INT NOT NULL,
  price NUMERIC NOT NULL,
  description TEXT,
  FOREIGN KEY (seller_name) REFERENCES Users(username)
);

CREATE TABLE TransactionHistory (
  id SERIAL PRIMARY KEY,
  buyer_id INT NOT NULL REFERENCES Users(id),
  seller_id INT NOT NULL REFERENCES Users(id),
  product_name TEXT NOT NULL,
  quantity INT NOT NULL,
  price NUMERIC NOT NULL,
  timestamp TIMESTAMP DEFAULT NOW()
);
