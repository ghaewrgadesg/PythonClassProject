USE InformationManagementSystem;
-- -----------------------------------------------------
-- adding data to `InformationManagementSystem`.`Users`
-- -----------------------------------------------------
INSERT INTO `Users` (`email`, `name`, `username`, `password`) VALUES ('bthung2003@gmail.com', 'BTH', 'bthung2003', 'SeeTheLight');
INSERT INTO `Users` (`email`, `name`, `username`, `password`) VALUES ('bthung2420@gmail.com', 'BTD', 'duyngu2003', 'KillTheLight');

-- -----------------------------------------------------
-- adding data to `InformationManagementSystem`.`Project`
-- -----------------------------------------------------
INSERT INTO `Project` (`name`, `manager_email`, `start_date`, `end_date`) VALUES('Killing the world', 'bthung2003@gmail.com', '2023-4-20', '2023-5-20');

-- -----------------------------------------------------
-- adding data to `InformationManagementSystem`.`Tasks`
-- -----------------------------------------------------
INSERT INTO `Tasks` (`name`, `project_name`, `cost`, `start_date`, `end_date`, `status`) VALUES('Test the water', 'Killing the world', 1000, '2023-4-23', '2023-4-26', 'IN PROGRESS');

-- -----------------------------------------------------
-- adding data to `InformationManagementSystem`.`ProjectBudget`
-- -----------------------------------------------------
INSERT INTO `ProjectBudget` (`project_name`, `potential_budget`, `planned_budget`) VALUES ('Killing the world', 100000, 200000);

-- -----------------------------------------------------
-- adding data to `InformationManagementSystem`.`ProjectMember`
-- -----------------------------------------------------
INSERT INTO `ProjectMember` (`member_email`, `project_name`) VALUES ('bthung2003@gmail.com','Killing the world');
INSERT INTO `ProjectMember` (`member_email`, `project_name`) VALUES ('bthung2420@gmail.com','Killing the world');

-- -----------------------------------------------------
-- adding data to `InformationManagementSystem`.`AssignedTaskMember`
-- -----------------------------------------------------
INSERT INTO `AssignedTaskMember` (`project_name`, `task_name`, `member_email`) VALUES ('Killing the world', 'Test the water', 'bthung2003@gmail.com')




