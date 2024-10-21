CREATE TABLE role (
    id SERIAL PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    permissions JSON NOT NULL
);

CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    login VARCHAR(30) UNIQUE NOT NULL,
    hashed_password VARCHAR(60) NOT NULL,
    role_id INTEGER NOT NULL,
    CONSTRAINT fk_role FOREIGN KEY (role_id) REFERENCES role(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);
