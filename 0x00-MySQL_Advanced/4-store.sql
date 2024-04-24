-- creates a trigger that decreases the quantity of an item after adding a new order.

CREATE TRIGGER decreases_quantity_on_order
AFTER INSERT ON orders
FOR EACH ROW
SET quantity = (quantity - NEW.number) WHERE name=NEW.item_name;
