-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: db:3306
-- Generation Time: Dec 12, 2024 at 12:16 AM
-- Server version: 8.0.34
-- PHP Version: 8.2.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `vempatd_project_management_tool`
--

-- --------------------------------------------------------

--
-- Table structure for table `Comments`
--

CREATE TABLE `Comments` (
  `comment_id` int NOT NULL,
  `content` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `updated_on` datetime DEFAULT NULL,
  `task_id` int DEFAULT NULL,
  `user_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `Comments`
--

INSERT INTO `Comments` (`comment_id`, `content`, `updated_on`, `task_id`, `user_id`) VALUES
(1, 'Made the first 3 views of the application using Figma and it put out for review', '2024-01-01 00:00:00', 41, 3),
(2, 'Modified UI on managers feedback', '2024-02-02 00:00:00', 41, 3),
(42, 'Worked on view 4 and view 5 of the application design. ', '2024-02-02 00:00:00', 41, 4),
(43, 'tested get call for API -1 ', '2024-12-10 00:00:00', 35, 5),
(44, 'dss', '2024-12-12 00:00:00', 41, 2),
(45, 'dsdsd', '2024-12-12 00:00:00', 41, 2),
(46, 'load test ', '2024-12-12 00:00:00', 41, 2),
(47, 'laod test', '2024-12-12 00:00:00', 41, 2),
(48, 'qwer', '2024-12-12 00:00:00', 41, 2),
(49, 'ewq', '2024-12-12 00:00:00', 41, 2),
(50, 'qwerty', '2024-12-12 00:00:00', 41, 2),
(51, 'load test', '2024-12-12 00:00:00', 41, 2),
(52, 'perfmest a test for get/APi of orders', '2024-12-12 00:00:00', 37, 3);

-- --------------------------------------------------------

--
-- Table structure for table `Task`
--

CREATE TABLE `Task` (
  `task_id` int NOT NULL,
  `task_name` varchar(50) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `status` varchar(50) NOT NULL,
  `created_on` datetime DEFAULT CURRENT_TIMESTAMP,
  `due_date` datetime DEFAULT NULL,
  `updated_on` datetime DEFAULT NULL,
  `priority` varchar(50) NOT NULL,
  `total_hours` int DEFAULT '0',
  `logged_hours` int DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `Task`
--

INSERT INTO `Task` (`task_id`, `task_name`, `description`, `status`, `created_on`, `due_date`, `updated_on`, `priority`, `total_hours`, `logged_hours`) VALUES
(35, 'performance test', 'testing the turn around time for each API', 'In Progress', '2024-11-05 00:00:00', '2024-12-18 00:00:00', '2024-12-11 00:00:00', 'High', 60, 50),
(37, 'smoke test', 'perform smoke test', 'In Progress', '2024-12-02 00:00:00', '2024-12-25 00:00:00', '2024-12-12 00:00:00', 'Medium', 30, 16),
(38, 'get old order details', 'feature addition to api', 'Not Started', '2024-12-04 00:00:00', '2024-12-25 00:00:00', '2024-12-04 00:00:00', 'Medium', 100, 120),
(39, 'deployment', 'package the application and deploy the app', 'Completed', '2024-12-04 00:00:00', '2024-12-31 00:00:00', '2024-12-04 00:00:00', 'Low', 50, 50),
(41, 'Ui design report', 'Give initial design of the application', 'Completed', '2024-12-01 00:00:00', '2024-12-31 00:00:00', '2024-12-12 00:00:00', 'High', 50, 11);

-- --------------------------------------------------------

--
-- Table structure for table `Users`
--

CREATE TABLE `Users` (
  `user_id` int NOT NULL,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` varchar(50) NOT NULL,
  `doj` date NOT NULL,
  `Active` varchar(4) NOT NULL DEFAULT 'Yes'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `Users`
--

INSERT INTO `Users` (`user_id`, `name`, `password`, `role`, `doj`, `Active`) VALUES
(1, 'admin_1', '4b959d44685d95c71d096758a7bb0b1d', 'admin', '2024-10-10', 'Yes'),
(2, 'manager_1', '4b959d44685d95c71d096758a7bb0b1d', 'manager', '2024-11-11', 'Yes'),
(3, 'employee_1', '4b959d44685d95c71d096758a7bb0b1d', 'employee', '2024-11-13', 'Yes'),
(4, 'employee_2', '4b959d44685d95c71d096758a7bb0b1d', 'employee', '2024-11-14', 'Yes'),
(5, 'nipun01', '4b959d44685d95c71d096758a7bb0b1d', 'employee', '2024-11-20', 'No'),
(17, 'tyler', '4b959d44685d95c71d096758a7bb0b1d', 'employee', '2024-12-11', 'Yes'),
(18, 'nipun', '4b959d44685d95c71d096758a7bb0b1d', 'employee', '2024-12-10', 'Yes');

-- --------------------------------------------------------

--
-- Table structure for table `User_tasks`
--

CREATE TABLE `User_tasks` (
  `user_task_id` int NOT NULL,
  `user_id` int DEFAULT NULL,
  `task_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `User_tasks`
--

INSERT INTO `User_tasks` (`user_task_id`, `user_id`, `task_id`) VALUES
(59, 3, 35),
(60, 4, 35),
(61, 3, 37),
(62, 4, 37),
(64, 3, 39),
(65, 4, 39),
(66, 5, 39),
(67, 3, 38),
(68, 4, 38),
(71, 3, 41);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Comments`
--
ALTER TABLE `Comments`
  ADD PRIMARY KEY (`comment_id`),
  ADD KEY `task_id` (`task_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `Task`
--
ALTER TABLE `Task`
  ADD PRIMARY KEY (`task_id`);

--
-- Indexes for table `Users`
--
ALTER TABLE `Users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `username` (`name`);

--
-- Indexes for table `User_tasks`
--
ALTER TABLE `User_tasks`
  ADD PRIMARY KEY (`user_task_id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `task_id` (`task_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Comments`
--
ALTER TABLE `Comments`
  MODIFY `comment_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=53;

--
-- AUTO_INCREMENT for table `Task`
--
ALTER TABLE `Task`
  MODIFY `task_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=42;

--
-- AUTO_INCREMENT for table `Users`
--
ALTER TABLE `Users`
  MODIFY `user_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `User_tasks`
--
ALTER TABLE `User_tasks`
  MODIFY `user_task_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=72;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `Comments`
--
ALTER TABLE `Comments`
  ADD CONSTRAINT `Comments_ibfk_1` FOREIGN KEY (`task_id`) REFERENCES `Task` (`task_id`),
  ADD CONSTRAINT `Comments_ibfk_3` FOREIGN KEY (`user_id`) REFERENCES `Users` (`user_id`);

--
-- Constraints for table `User_tasks`
--
ALTER TABLE `User_tasks`
  ADD CONSTRAINT `User_tasks_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `Users` (`user_id`),
  ADD CONSTRAINT `User_tasks_ibfk_2` FOREIGN KEY (`task_id`) REFERENCES `Task` (`task_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
