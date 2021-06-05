-- DROP DATABASE IF EXISTS `gogolook`;
CREATE DATABASE IF NOT EXISTS `gogolook` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
START TRANSACTION;
USE `gogolook`;

drop table if exists gogolook.tasks;
create table gogolook.tasks(
    `id` INT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(20) NOT NULL,
    `status` BOOLEAN DEFAULT false,
    PRIMARY KEY ( `id` )
)engine=InnoDB default charset=utf8mb4 collate utf8mb4_general_ci comment='任務';
    

COMMIT;
