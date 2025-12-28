CREATE SCHEMA IF NOT EXISTS public;
SET search_path TO PUBLIC;

-- Fuel Types
CREATE TABLE fuel_types (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  price_per_unit NUMERIC NOT NULL
);

-- Refineries
CREATE TABLE refineries (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  address_line TEXT NOT NULL
);

-- Refinery Tanks
CREATE TABLE refinery_tanks (
  id SERIAL PRIMARY KEY,
  refinery_id INTEGER NOT NULL REFERENCES refineries(id),
  fuel_type_id INTEGER NOT NULL REFERENCES fuel_types(id),
  capacity NUMERIC NOT NULL,
  current_volume NUMERIC NOT NULL
);

-- Stations
CREATE TABLE stations (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  address TEXT NOT NULL,
  contact_number TEXT NOT NULL
);

-- Station Tanks
CREATE TABLE station_tanks (
  id SERIAL PRIMARY KEY,
  station_id INTEGER NOT NULL REFERENCES stations(id),
  fuel_type_id INTEGER NOT NULL REFERENCES fuel_types(id),
  capacity NUMERIC NOT NULL,
  current_volume NUMERIC NOT NULL
);

-- Providers
CREATE TABLE providers (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  details TEXT
);

-- Payment Methods
CREATE TABLE payment_methods (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  slug TEXT NOT NULL UNIQUE,
  type TEXT NOT NULL,
  is_active BOOLEAN NOT NULL,
  requires_authorization BOOLEAN NOT NULL,
  provider_id INTEGER REFERENCES providers(id)
);

-- Sale Transaction Statuses
CREATE TABLE sale_transaction_statuses (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL
);

-- Client Tiers
CREATE TABLE client_tiers (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT
);

-- Customers
CREATE TABLE customers (
  id SERIAL PRIMARY KEY,
  phone_number TEXT NOT NULL UNIQUE,
  registration_date DATE NOT NULL,
  bonus_points INTEGER NOT NULL DEFAULT 0,
  client_tier_id INTEGER REFERENCES client_tiers(id),
  total_purchases NUMERIC NOT NULL DEFAULT 0,
  last_visit_date DATE
);

-- Operator Statuses
CREATE TABLE operator_statuses (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL
);

-- Operator Roles
CREATE TABLE operator_roles (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  descryption TEXT
);

-- Operators
CREATE TABLE operators (
  id SERIAL PRIMARY KEY,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  phone_number TEXT,
  email TEXT,
  status_id INTEGER NOT NULL REFERENCES operator_statuses(id),
  role_id INTEGER NOT NULL REFERENCES operator_roles(id),
  password_hash TEXT NOT NULL
);

-- Sale Transactions
CREATE TABLE sale_transactions (
  id SERIAL PRIMARY KEY,
  customer_id INTEGER REFERENCES customers(id),
  operator_id INTEGER NOT NULL REFERENCES operators(id),
  payment_method_id INTEGER NOT NULL REFERENCES payment_methods(id),
  total_amount NUMERIC NOT NULL,
  transaction_date_time TIMESTAMP NOT NULL,
  bonus_used INTEGER DEFAULT 0,
  volume NUMERIC NOT NULL,
  currency TEXT NOT NULL,
  status_id INTEGER NOT NULL REFERENCES sale_transaction_statuses(id)
);

-- Sale Transaction Audit
CREATE TABLE sale_transaction_audit (
  id SERIAL PRIMARY KEY,
  sale_transaction_id INTEGER NOT NULL REFERENCES sale_transactions(id),
  changed_at TIMESTAMP NOT NULL,
  old_status_id INTEGER REFERENCES sale_transaction_statuses(id),
  new_status_id INTEGER NOT NULL REFERENCES sale_transaction_statuses(id),
  comments TEXT
);

-- Refueling Session Statuses
CREATE TABLE refueling_session_statuses (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL
);

-- Fuel Dispensers
CREATE TABLE fuel_dispensers (
  id SERIAL PRIMARY KEY,
  station_id INTEGER NOT NULL REFERENCES stations(id),
  is_active BOOLEAN NOT NULL
);

-- Fuel Pumps
CREATE TABLE fuel_pumps (
  id SERIAL PRIMARY KEY,
  fuel_type_id INTEGER NOT NULL REFERENCES fuel_types(id),
  fuel_dispenser_id INTEGER NOT NULL REFERENCES fuel_dispensers(id),
  nozzle_number INTEGER NOT NULL,
  is_active BOOLEAN NOT NULL
);

-- Refueling Sessions
CREATE TABLE refueling_sessions (
  id SERIAL PRIMARY KEY,
  fuel_pump_id INTEGER NOT NULL REFERENCES fuel_pumps(id),
  fuel_type_id INTEGER NOT NULL REFERENCES fuel_types(id),
  volume NUMERIC NOT NULL,
  authorized_volume NUMERIC,
  started_at TIMESTAMP NOT NULL,
  finished_at TIMESTAMP,
  status_id INTEGER NOT NULL REFERENCES refueling_session_statuses(id),
  sale_transaction_id INTEGER NOT NULL REFERENCES sale_transactions(id)
);

-- Storage Locations
CREATE TABLE storage_locations (
  id SERIAL PRIMARY KEY,
  refinery_id INTEGER NOT NULL REFERENCES refineries(id),
  name TEXT NOT NULL
);

-- Production Unit Statuses
CREATE TABLE production_unit_statuses (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL
);

-- Production Units
CREATE TABLE production_units (
  id SERIAL PRIMARY KEY,
  refinery_id INTEGER NOT NULL REFERENCES refineries(id),
  name TEXT NOT NULL,
  capacity_per_day NUMERIC NOT NULL,
  last_maintenance DATE,
  status_id INTEGER NOT NULL REFERENCES production_unit_statuses(id)
);

-- Order Statuses
CREATE TABLE order_statuses (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL
);

-- Batch Statuses
CREATE TABLE batch_statuses (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL
);

-- Production Batches
CREATE TABLE production_batches (
  id SERIAL PRIMARY KEY,
  start_time TIMESTAMP NOT NULL,
  end_time TIMESTAMP,
  expected_output_volume NUMERIC NOT NULL,
  status_id INTEGER NOT NULL REFERENCES batch_statuses(id)
);

-- Production Batch Tank Refineries
CREATE TABLE production_batch_tank_refineries (
  production_batch_id INTEGER NOT NULL REFERENCES production_batches(id),
  refinery_tank_id INTEGER NOT NULL REFERENCES refinery_tanks(id),
  PRIMARY KEY (production_batch_id, refinery_tank_id)
);

-- Suppliers
CREATE TABLE suppliers (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  type TEXT NOT NULL
);

-- Raw Materials
CREATE TABLE raw_materials (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  type TEXT NOT NULL,
  quality_parameter TEXT,
  price_per_unit NUMERIC NOT NULL,
  unit TEXT NOT NULL
);

-- Raw Materials Supply
CREATE TABLE raw_materials_supply (
  id SERIAL PRIMARY KEY,
  supplier_id INTEGER NOT NULL REFERENCES suppliers(id),
  raw_material_id INTEGER NOT NULL REFERENCES raw_materials(id),
  refinery_id INTEGER NOT NULL REFERENCES refineries(id),
  delivery_date DATE NOT NULL,
  created_at TIMESTAMP NOT NULL,
  quantity NUMERIC NOT NULL,
  quality_check_passed BOOLEAN,
  status_id INTEGER NOT NULL REFERENCES order_statuses(id)
);

-- Raw Materials Deliveries
CREATE TABLE raw_materials_deliveries (
  id SERIAL PRIMARY KEY,
  supply_id INTEGER NOT NULL REFERENCES raw_materials_supply(id),
  received_at TIMESTAMP NOT NULL
);

-- Delivery Items
CREATE TABLE delivery_items (
  id SERIAL PRIMARY KEY,
  delivery_id INTEGER NOT NULL REFERENCES raw_materials_deliveries(id),
  storage_location_id INTEGER NOT NULL REFERENCES storage_locations(id),
  raw_material_id INTEGER NOT NULL REFERENCES raw_materials(id),
  deliveried_at TIMESTAMP NOT NULL
);

-- Production Batch Raw Materials
CREATE TABLE production_batch_raw_materials (
  production_batch_id INTEGER NOT NULL REFERENCES production_batches(id),
  delivery_item_id INTEGER NOT NULL REFERENCES delivery_items(id),
  volume NUMERIC NOT NULL,
  PRIMARY KEY (production_batch_id, delivery_item_id)
);

-- Production Batch Units
CREATE TABLE production_batch_units (
  production_batch_id INTEGER NOT NULL REFERENCES production_batches(id),
  production_unit_id INTEGER NOT NULL REFERENCES production_units(id),
  start_time TIMESTAMP NOT NULL,
  end_time TIMESTAMP,
  PRIMARY KEY (production_batch_id, production_unit_id)
);

-- Tank Types
CREATE TABLE tank_types (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT
);

-- Transfer Statuses
CREATE TABLE transfer_statuses (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL
);

-- Order Types
CREATE TABLE order_types (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT
);

-- Transport Statuses
CREATE TABLE transport_statuses (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL
);

-- Transports
CREATE TABLE transports (
  id SERIAL PRIMARY KEY,
  transport_number TEXT NOT NULL,
  transport_type TEXT NOT NULL,
  capacity NUMERIC NOT NULL,
  status INTEGER NOT NULL REFERENCES transport_statuses(id),
  current_location TEXT
);

-- Terminals
CREATE TABLE terminals (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  address_line TEXT NOT NULL
);

-- Terminal Tanks
CREATE TABLE terminal_tanks (
  id SERIAL PRIMARY KEY,
  terminal_id INTEGER NOT NULL REFERENCES terminals(id),
  fuel_type_id INTEGER NOT NULL REFERENCES fuel_types(id),
  capacity NUMERIC NOT NULL,
  current_volume NUMERIC NOT NULL
);

-- Supply Orders
CREATE TABLE supply_orders (
  id SERIAL PRIMARY KEY,
  fuel_type_id INTEGER NOT NULL REFERENCES fuel_types(id),
  created_at TIMESTAMP NOT NULL,
  supply_date DATE NOT NULL,
  station_id INTEGER NOT NULL REFERENCES stations(id),
  status_id INTEGER NOT NULL REFERENCES order_statuses(id)
);

-- Production Orders
CREATE TABLE production_orders (
  id SERIAL PRIMARY KEY,
  terminal_id INTEGER NOT NULL REFERENCES terminals(id),
  fuel_type_id INTEGER NOT NULL REFERENCES fuel_types(id),
  refinery_id INTEGER NOT NULL REFERENCES refineries(id),
  volume_requested NUMERIC NOT NULL,
  created_at TIMESTAMP NOT NULL,
  required_by_date DATE NOT NULL,
  priority INTEGER NOT NULL,
  status_id INTEGER NOT NULL REFERENCES order_statuses(id)
);

-- Fuel Transfers
CREATE TABLE fuel_transfers (
  id SERIAL PRIMARY KEY,
  source_type_id INTEGER NOT NULL REFERENCES tank_types(id),
  source_id INTEGER NOT NULL,
  destination_type_id INTEGER NOT NULL REFERENCES tank_types(id),
  destination_id INTEGER NOT NULL,
  order_type_id INTEGER NOT NULL REFERENCES order_types(id),
  order_id INTEGER NOT NULL,
  volume NUMERIC NOT NULL,
  dispatched_at TIMESTAMP NOT NULL,
  received_at TIMESTAMP,
  status_id INTEGER NOT NULL REFERENCES transfer_statuses(id)
);

-- Transfer Transports
CREATE TABLE transfer_transports (
  transfer_id INTEGER NOT NULL REFERENCES fuel_transfers(id),
  transport_id INTEGER NOT NULL REFERENCES transports(id),
  volume NUMERIC NOT NULL,
  PRIMARY KEY (transfer_id, transport_id)
);
