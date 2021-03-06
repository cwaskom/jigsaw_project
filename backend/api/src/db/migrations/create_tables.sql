DROP TABLE IF EXISTS hotels CASCADE;
DROP TABLE IF EXISTS chains CASCADE;
DROP TABLE IF EXISTS locations CASCADE;
DROP TABLE IF EXISTS offers CASCADE;
DROP TABLE IF EXISTS descriptions CASCADE;

CREATE TABLE IF NOT EXISTS locations (
  id serial PRIMARY KEY,
  lon DECIMAL,
  lat DECIMAL,
  address VARCHAR(255) NOT NULL,
  city_name VARCHAR(255) NOT NULL,
  postal_code VARCHAR(255),
  country_code VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS chains (
  id serial PRIMARY KEY,
  chain_code VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS hotels (
  id serial PRIMARY KEY,
  amadeus_id VARCHAR(255) UNIQUE,
  name VARCHAR(255) NOT NULL,
  location_id INTEGER,
  chain_id VARCHAR(255) NOT NULL,
  rating DECIMAL,
  CONSTRAINT fk_location
    FOREIGN KEY (location_id)
      REFERENCES locations (id) ON DELETE CASCADE
  -- CONSTRAINT fk_chain_id
  --   FOREIGN KEY (chain_id)
  --     REFERENCES chains (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS offers (
  id serial PRIMARY KEY,
  hotel_id INTEGER,
  offer_id VARCHAR(255) NOT NULL,
  check_in DATE NOT NULL,
  check_out DATE NOT NULL,
  available BOOLEAN NOT NULL,
  currency VARCHAR(255) NOT NULL,
  total_rate DECIMAL NOT NULL, 
  comm_percentage DECIMAL,
  created_at TIMESTAMP DEFAULT NOW(),
  CONSTRAINT fk_hotel_id
    FOREIGN KEY (hotel_id)
      REFERENCES hotels (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS descriptions (
  id serial PRIMARY KEY,
  hotel_id INTEGER,
  description VARCHAR(500) NOT NULL,
  amenities VARCHAR(255) NOT NULL,
  media_uri VARCHAR(255) NOT NULL,
  CONSTRAINT fk_hotel_id
    FOREIGN KEY (hotel_id)
      REFERENCES hotels (id) ON DELETE CASCADE
);