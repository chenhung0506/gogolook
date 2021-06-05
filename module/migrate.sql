CREATE DATABASE IF NOT EXISTS `migrate` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
START TRANSACTION;

DROP TABLE IF EXISTS migrate.migrate;
CREATE TABLE migrate.migrate(
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(20) NOT NULL,
    init_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY ( id )
)engine=InnoDB default charset=utf8mb4 collate utf8mb4_general_ci comment='migrate';

COMMIT;