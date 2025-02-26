CREATE TABLE IF NOT EXISTS users
(
    id   SERIAL PRIMARY KEY,
    name VARCHAR(100),
    age  INT
);

CREATE TABLE IF NOT EXISTS orders
(
    id      SERIAL PRIMARY KEY,
    user_id INT REFERENCES users (id),
    amount  DECIMAL(10, 2)
);

INSERT INTO users (name, age)
SELECT 'User_' || generate_series(1, 100),
       floor(random() * 50 + 20)::int
FROM generate_series(1, 10);


INSERT INTO orders (user_id, amount)
SELECT floor(random() * 100 + 1)::int,
       round((random() * 500 + 10)::numeric, 2)
FROM generate_series(1, 100);
