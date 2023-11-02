-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 01, 2023 at 01:11 PM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.1.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `nasme`
--

-- --------------------------------------------------------

--
-- Table structure for table `message`
--

CREATE TABLE `message` (
  `id` int(11) NOT NULL,
  `sender_id` int(11) DEFAULT NULL,
  `member_recipient_id` int(11) DEFAULT NULL,
  `unit_recipient_id` int(11) DEFAULT NULL,
  `title` varchar(60) DEFAULT NULL,
  `body` varchar(500) DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `message`
--

INSERT INTO `message` (`id`, `sender_id`, `member_recipient_id`, `unit_recipient_id`, `title`, `body`, `timestamp`) VALUES
(1, 1, 12, NULL, 'MY FIRST MESSAGE', 'Hey, MLT. \r\nI got to know that you\'re actually in need of a way to get your stuff ready to fill i with the stuffs.', '2023-10-30 15:39:32');

-- --------------------------------------------------------

--
-- Table structure for table `unit`
--

CREATE TABLE `unit` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `date_created` datetime NOT NULL,
  `fees_amount` varchar(77) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `unit`
--

INSERT INTO `unit` (`id`, `name`, `date_created`, `fees_amount`) VALUES
(1, 'firstunit', '2023-10-27 15:37:30', '');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(20) DEFAULT NULL,
  `email` varchar(120) DEFAULT NULL,
  `phone` varchar(60) DEFAULT NULL,
  `password` varchar(60) NOT NULL,
  `image_file` varchar(20) NOT NULL,
  `date_registered` datetime NOT NULL,
  `role` varchar(6) NOT NULL,
  `is_superadmin` tinyint(1) NOT NULL,
  `current_salary` varchar(60) DEFAULT NULL,
  `occupation` varchar(60) DEFAULT NULL,
  `experience` varchar(60) DEFAULT NULL,
  `date_of_birth` varchar(77) NOT NULL,
  `business_address` varchar(120) DEFAULT NULL,
  `is_suspended` tinyint(1) NOT NULL,
  `has_filled_profile` tinyint(1) DEFAULT NULL,
  `business_name` varchar(77) DEFAULT NULL,
  `business_email` varchar(120) DEFAULT NULL,
  `business_phone` varchar(77) DEFAULT NULL,
  `business_photo` varchar(20) DEFAULT NULL,
  `business_about` varchar(300) DEFAULT NULL,
  `business_services` varchar(300) DEFAULT NULL,
  `business_product_image_1` varchar(20) NOT NULL,
  `business_product_image_2` varchar(20) NOT NULL,
  `business_product_image_3` varchar(20) NOT NULL,
  `business_product_image_4` varchar(20) NOT NULL,
  `business_product_image_5` varchar(20) NOT NULL,
  `business_product_image_6` varchar(20) NOT NULL,
  `business_facebook` varchar(77) DEFAULT NULL,
  `business_website` varchar(77) DEFAULT NULL,
  `business_twitter` varchar(77) DEFAULT NULL,
  `business_linkedin` varchar(77) DEFAULT NULL,
  `business_whatsapp` varchar(77) DEFAULT NULL,
  `last_message_read_time` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `username`, `email`, `phone`, `password`, `image_file`, `date_registered`, `role`, `is_superadmin`, `current_salary`, `occupation`, `experience`, `date_of_birth`, `business_address`, `is_suspended`, `has_filled_profile`, `business_name`, `business_email`, `business_phone`, `business_photo`, `business_about`, `business_services`, `business_product_image_1`, `business_product_image_2`, `business_product_image_3`, `business_product_image_4`, `business_product_image_5`, `business_product_image_6`, `business_facebook`, `business_website`, `business_twitter`, `business_linkedin`, `business_whatsapp`, `last_message_read_time`) VALUES
(1, 'superadmin', 'super@admin.com', '09078792471', 'superadmin', '', '2023-10-27 15:38:04', 'ADMIN', 1, '600000', 'Teacher', '19 years', '', NULL, 0, 1, NULL, NULL, NULL, NULL, NULL, NULL, '', '', '', '', '', '', NULL, NULL, NULL, NULL, NULL, NULL),
(11, NULL, 'fsaweruhrwe@jjfdjdf.com', '2238732732', '1234567890', '18cf0468515878f9.JPG', '2023-10-30 11:07:03', 'USER', 0, NULL, NULL, NULL, '2023-10-30 11:07:03.245224', '23j af afkldoijioaalkfafsdkfalf ati idiroko', 0, 0, 'Rice Bu', 'changedagain@tobbs.com', '2838928933987', 'c6689f93698d0a42.JPG', 'dsfadafasklsdfllweewr ', 'I don\'t have any services', '1b730294e956cc73.JPG', 'b0e86c439a98ebf8.JPG', 'default.jpg', 'default.jpg', 'default.jpg', 'default.jpg', 'facebook.com', 'www.htl.com', 'well.com', 'slt.com', 'web.com', NULL),
(12, NULL, 'superfluous@admin.com', '909034483723', '1234567890', '825f73cc6cce590b.jpg', '2023-10-30 11:07:50', 'USER', 0, NULL, NULL, NULL, '2023-10-30 11:07:50.864497', '23j af afkldoijioaalkfafsdkfalf', 0, 0, 'MLTt', 'atthefoot@gmail.com', '2232377378387338893', 'bf89fc73e12a58c1.jpg', 'This is a whole new business', 'This is nothing known to me.', '55fe5233e35bfccd.JPG', 'default.jpg', '8cf3910f0cf93b6a.JPG', 'default.jpg', 'default.jpg', 'default.jpg', 'fetherine.com', 'wellim.com', 'tweetit.com', 'linkedinit.com', 'whatsappbro.com', '2023-10-30 15:39:50'),
(14, NULL, NULL, NULL, '12345678', '', '2023-10-30 15:35:29', 'USER', 0, NULL, NULL, NULL, '2023-10-30 15:35:29.448074', NULL, 0, 0, NULL, NULL, NULL, 'default.jpg', NULL, NULL, 'default.jpg', 'default.jpg', 'default.jpg', 'default.jpg', 'default.jpg', 'default.jpg', NULL, NULL, NULL, NULL, NULL, NULL),
(15, NULL, NULL, NULL, '12345678', '', '2023-10-30 15:35:29', 'USER', 0, NULL, NULL, NULL, '2023-10-30 15:35:29.480898', NULL, 0, 0, NULL, NULL, NULL, 'default.jpg', NULL, NULL, 'default.jpg', 'default.jpg', 'default.jpg', 'default.jpg', 'default.jpg', 'default.jpg', NULL, NULL, NULL, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `user_unit`
--

CREATE TABLE `user_unit` (
  `user_id` int(11) DEFAULT NULL,
  `unit_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_unit`
--

INSERT INTO `user_unit` (`user_id`, `unit_id`) VALUES
(11, 1),
(12, 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `message`
--
ALTER TABLE `message`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sender_id` (`sender_id`),
  ADD KEY `member_recipient_id` (`member_recipient_id`),
  ADD KEY `unit_recipient_id` (`unit_recipient_id`),
  ADD KEY `ix_message_timestamp` (`timestamp`);

--
-- Indexes for table `unit`
--
ALTER TABLE `unit`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `phone` (`phone`);

--
-- Indexes for table `user_unit`
--
ALTER TABLE `user_unit`
  ADD KEY `user_id` (`user_id`),
  ADD KEY `unit_id` (`unit_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `message`
--
ALTER TABLE `message`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `unit`
--
ALTER TABLE `unit`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `message`
--
ALTER TABLE `message`
  ADD CONSTRAINT `message_ibfk_1` FOREIGN KEY (`sender_id`) REFERENCES `user` (`id`),
  ADD CONSTRAINT `message_ibfk_2` FOREIGN KEY (`member_recipient_id`) REFERENCES `user` (`id`),
  ADD CONSTRAINT `message_ibfk_3` FOREIGN KEY (`unit_recipient_id`) REFERENCES `unit` (`id`);

--
-- Constraints for table `user_unit`
--
ALTER TABLE `user_unit`
  ADD CONSTRAINT `user_unit_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  ADD CONSTRAINT `user_unit_ibfk_2` FOREIGN KEY (`unit_id`) REFERENCES `unit` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
