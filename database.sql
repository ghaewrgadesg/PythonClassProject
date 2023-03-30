Drop database if exists InformationManagementSystem;
CREATE DATABASE InformationManagementSystem;
USE InformationManagementSystem;
-- -----------------------------------------------------
-- Table `InformationManagementSystem`.`Users`
-- -----------------------------------------------------
create table if not exists `Users`(
	`email` varchar(254) NOT NULL,
    `name` varchar(50) NOT NULL,
    `username` varchar(50) NOT NULL,
    `password` varchar(100) NOT NULL,
    Primary key (`email`),
    Unique( `name`, `username`, `password`)
);

-- -----------------------------------------------------
-- Table `InformationManagementSystem`.`Project`
-- -----------------------------------------------------
create table if not exists `Project`(
	`name` varchar(200) NOT NULL,
    `manager_email` varchar(254) NOT NULL,
    `start_date` date NOT NULL,
    `end_date` date NOT NULL,
    `description` text,
    Primary key (`name`),
    foreign key (`manager_email`) references Users(`email`)
);

    
-- -----------------------------------------------------
-- Table `InformationManagementSystem`.`Tasks`
-- -----------------------------------------------------
create table if not exists `Tasks`(
	`name` varchar(100) NOT NULL,
    `project_name` varchar(200) NOT NULL,
    `cost` int NOT NULL,
    `start_date` date NOT NULL,
    `end_date` date NOT NULL,
    `status` varchar(20) NOT NULL,
    `description` text,
    Primary key(`name`,`project_name`),
    foreign key (`project_name`) references Project(`name`)
);

-- -----------------------------------------------------
-- Table `InformationManagementSystem`.`ProjectBudget`
-- -----------------------------------------------------
create table if not exists `ProjectBudget`(
	`project_name` varchar(200) NOT NULL,
    `potential_budget` int NOT NULL,
    `plan_budget` int NOT NULL,
    foreign key (`project_name`) references Project(`name`)
);

-- -----------------------------------------------------
-- Table `InformationManagementSystem`.`ProjectMember`
-- -----------------------------------------------------
create table if not exists `ProjectMember`(
	`member_email` varchar(254) NOT NULL,
    `project_name` varchar(200) NOT NULL,
    foreign key (`member_email`) references Users(`email`),
    foreign key (`project_name`) references Project(`name`)
	
);
    
-- -----------------------------------------------------
-- Table `InformationManagementSystem`.`AssignedTaskMember`
-- -----------------------------------------------------
create table if not exists `AssignedTaskMember`(
	`member_email` varchar(254) NOT NULL,
    `project_name` varchar(200) NOT NULL,
    `task_name` varchar(100) NOT NULL,
    primary key(`task_name`, `member_email`, `project_name`),
    foreign key (`task_name`) references Tasks(`name`),
    foreign key (`member_email`) references Users(`email`),
    foreign key (`project_name`) references Project(`name`)
    
);
	