-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 02, 2025 at 09:02 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `pos_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `category_list`
--

CREATE TABLE `category_list` (
  `CategoryID` int(30) NOT NULL,
  `name` text NOT NULL,
  `Description` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `category_list`
--

INSERT INTO `category_list` (`CategoryID`, `name`, `Description`) VALUES
(1, 'Drink', NULL),
(2, 'Layer', NULL),
(3, 'Soya', NULL),
(4, 'Palm', NULL),
(5, 'Vegetables', NULL),
(6, 'Fruits', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `customer_list`
--

CREATE TABLE `customer_list` (
  `CustomerID` int(30) NOT NULL,
  `name` text NOT NULL,
  `role` varchar(50) DEFAULT NULL,
  `contact` varchar(30) NOT NULL,
  `address` text NOT NULL,
  `loyaltypoints` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `customer_list`
--

INSERT INTO `customer_list` (`CustomerID`, `name`, `role`, `contact`, `address`, `loyaltypoints`) VALUES
(1, 'John Smith', NULL, '8747808787', 'Sample Only', NULL),
(2, 'George Wilson', NULL, '+14526-5455-44', 'Sample', NULL),
(3, 'Kennedy Lubega', NULL, '0759623689', 'Kamengo', 0);

-- --------------------------------------------------------

--
-- Table structure for table `inventory`
--

CREATE TABLE `inventory` (
  `id` int(30) NOT NULL,
  `product_id` int(30) NOT NULL,
  `qty` int(30) NOT NULL,
  `type` tinyint(1) NOT NULL COMMENT '1= stockin , 2 = stockout',
  `stock_from` varchar(100) NOT NULL COMMENT 'sales/receiving',
  `form_id` int(30) NOT NULL,
  `other_details` text NOT NULL,
  `remarks` text NOT NULL,
  `date_updated` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `inventory`
--

INSERT INTO `inventory` (`id`, `product_id`, `qty`, `type`, `stock_from`, `form_id`, `other_details`, `remarks`, `date_updated`) VALUES
(1, 1, 50, 1, 'receiving', 1, '{\"price\":\"70\",\"qty\":\"50\"}', 'Stock from Receiving-04377352\r\n', '2020-09-22 11:51:28'),
(8, 4, 50, 1, 'receiving', 1, '{\"price\":\"20\",\"qty\":\"50\"}', 'Stock from Receiving-04377352\r\n', '2020-09-22 11:51:42'),
(10, 5, 100, 1, 'receiving', 1, '{\"price\":\"20\",\"qty\":\"100\"}', 'Stock from Receiving-04377352\r\n', '2020-09-22 11:53:11'),
(11, 3, 100, 1, 'receiving', 1, '{\"price\":\"30\",\"qty\":\"100\"}', 'Stock from Receiving-04377352\r\n', '2020-09-22 11:53:11'),
(13, 4, 10, 2, 'Sales', 1, '{\"price\":\"10\",\"qty\":\"10\"}', 'Stock out from Sales-00000000\r\n', '2020-09-22 15:23:02'),
(14, 4, 20, 2, 'Sales', 2, '{\"price\":\"10\",\"qty\":\"20\"}', 'Stock out from Sales-17671173\n', '2020-09-22 15:00:46'),
(15, 4, 10, 2, 'Sales', 3, '{\"price\":\"10\",\"qty\":\"10\"}', 'Stock out from Sales-16042993\n', '2020-09-22 15:01:55'),
(16, 1, 10, 2, 'Sales', 4, '{\"price\":\"75\",\"qty\":\"10\"}', 'Stock out from Sales-50470080\r\n', '2020-09-22 15:42:59'),
(18, 1, 2, 2, 'Sales', 0, '{\"price\":\"75\",\"qty\":\"2\"}', 'Stock out from Sales-00000000\r\n', '2020-09-22 15:19:22'),
(19, 1, 2, 2, 'Sales', 0, '{\"price\":\"75\",\"qty\":\"2\"}', 'Stock out from Sales-00000000\r\n', '2020-09-22 15:20:03'),
(20, 1, 2, 2, 'Sales', 1, '{\"price\":\"75\",\"qty\":\"2\"}', 'Stock out from Sales-00000000\r\n', '2020-09-22 15:23:02'),
(21, 3, 10, 2, 'Sales', 4, '{\"price\":\"30\",\"qty\":\"10\"}', 'Stock out from Sales-50470080\r\n', '2020-09-22 15:42:59'),
(22, 5, 5, 2, 'Sales', 4, '{\"price\":\"25\",\"qty\":\"5\"}', 'Stock out from Sales-50470080\r\n', '2020-09-22 15:42:59');

-- --------------------------------------------------------

--
-- Table structure for table `inventory_logs`
--

CREATE TABLE `inventory_logs` (
  `inventory_log_id` int(11) NOT NULL,
  `product_id` int(11) DEFAULT NULL,
  `quantity_change` int(11) NOT NULL,
  `log_date` datetime DEFAULT current_timestamp(),
  `reason` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `inventory_logs`
--

INSERT INTO `inventory_logs` (`inventory_log_id`, `product_id`, `quantity_change`, `log_date`, `reason`) VALUES
(1, 1, 2000, '2024-12-09 14:38:43', 'price update'),
(2, 1, 10, '2024-12-09 14:39:29', 'restock'),
(3, 1, 2000, '2024-12-09 14:40:20', 'price update'),
(4, 1, 30, '2024-12-09 14:41:58', 'restock'),
(5, 1, -5, '2024-12-09 14:42:15', 'sale'),
(6, 1, -1, '2024-12-09 14:47:35', 'sale'),
(7, 1, 2000, '2024-12-09 16:13:35', 'price update'),
(8, 11, -2, '2024-12-09 19:09:17', 'sale'),
(9, 4, -1, '2024-12-09 19:09:17', 'sale'),
(10, 10, -1, '2024-12-09 19:09:17', 'sale'),
(11, 5, -1, '2024-12-09 19:09:17', 'sale'),
(12, 8, -1, '2024-12-09 19:09:17', 'sale'),
(13, 1, 50, '2024-12-09 19:11:37', 'restock'),
(14, 2, -1, '2024-12-09 19:12:31', 'sale'),
(15, 1, -8, '2024-12-09 19:58:08', 'sale'),
(16, 2, -3, '2024-12-09 19:58:08', 'sale'),
(17, 4, -2, '2024-12-09 19:58:08', 'sale'),
(18, 2, -2, '2024-12-09 20:03:19', 'sale'),
(19, 3, 5000, '2024-12-09 20:29:20', 'price update'),
(20, 2, -2, '2024-12-10 05:13:02', 'sale'),
(21, 2, -5, '2024-12-14 17:53:24', 'sale'),
(22, 10, -5, '2025-01-02 04:54:03', 'sale'),
(23, 7, -5, '2025-01-02 10:53:36', 'sale'),
(24, 7, -4, '2025-01-02 10:53:36', 'sale'),
(25, 7, -1, '2025-01-02 10:53:36', 'sale'),
(26, 9, 20, '2025-01-02 10:57:54', 'restock'),
(27, 2, -5, '2025-01-02 10:59:06', 'sale');

-- --------------------------------------------------------

--
-- Table structure for table `product_list`
--

CREATE TABLE `product_list` (
  `ProductID` int(11) NOT NULL,
  `category_id` int(11) NOT NULL,
  `sku` varchar(50) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` text DEFAULT NULL,
  `quantity` int(11) NOT NULL,
  `reorder_level` int(11) NOT NULL,
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `product_list`
--

INSERT INTO `product_list` (`ProductID`, `category_id`, `sku`, `price`, `name`, `description`, `quantity`, `reorder_level`, `updated_at`) VALUES
(1, 1, '9163453', 2000.00, 'Flower', 'flower blue', 42, 10, '2024-12-09 16:58:08'),
(2, 1, '3459442', 5000.00, 'Croton', 'Croton', 32, 10, '2025-01-02 07:59:06'),
(3, 2, '7584442', 5000.00, 'Layer Green 12', 'Layer Green', 0, 10, '2024-12-09 17:29:20'),
(4, 1, '9744511', 5000.00, 'Layer Purple', 'Layer Purple', 47, 10, '2024-12-09 16:58:08'),
(5, 3, '4799904', 10000.00, 'Soya Yellow', 'Soya Yellow', 49, 10, '2024-12-09 16:09:17'),
(6, 1, '2136440', 25000.00, 'Bird of Paradise', 'Bird of Paradise', 50, 10, '2024-12-09 12:55:15'),
(7, 4, '6002907', 10000.00, 'Bamboo Palm', 'Bamboo Palm', 40, 10, '2025-01-02 07:53:36'),
(8, 1, '3326373', 30000.00, 'Syeard Giant', 'Syeard Giant', 49, 10, '2024-12-09 16:09:17'),
(9, 4, '5566566', 15000.00, 'Traveler Palm', 'Traveler Palm', 70, 10, '2025-01-02 07:57:54'),
(10, 4, '2235394', 7000.00, 'Royal Palm', 'Royal Palm', 44, 10, '2025-01-02 01:54:03'),
(11, 1, '9887331', 15000.00, 'Piranga Young ', 'Piranga Young ', 48, 10, '2024-12-09 16:09:17');

-- --------------------------------------------------------

--
-- Table structure for table `receiving_list`
--

CREATE TABLE `receiving_list` (
  `id` int(30) NOT NULL,
  `ref_no` varchar(100) NOT NULL,
  `supplier_id` int(30) NOT NULL,
  `total_amount` double NOT NULL,
  `date_added` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `receiving_list`
--

INSERT INTO `receiving_list` (`id`, `ref_no`, `supplier_id`, `total_amount`, `date_added`) VALUES
(1, '04377352\n', 3, 9500, '2020-09-22 11:16:00');

-- --------------------------------------------------------

--
-- Table structure for table `sales`
--

CREATE TABLE `sales` (
  `salesID` int(30) NOT NULL,
  `ProductID` varchar(30) NOT NULL,
  `customer_id` int(30) NOT NULL,
  `price` double NOT NULL,
  `discount` double DEFAULT NULL,
  `qty` int(30) NOT NULL,
  `discounted_price` double NOT NULL,
  `total_price` double NOT NULL,
  `date_updated` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sales`
--

INSERT INTO `sales` (`salesID`, `ProductID`, `customer_id`, `price`, `discount`, `qty`, `discounted_price`, `total_price`, `date_updated`) VALUES
(0, '10', 2, 35000, 0, 5, 35000, 175000, '2025-01-02 04:54:03'),
(0, '7', 1, 50000, 0, 5, 50000, 250000, '2025-01-02 10:53:35'),
(0, '7', 1, 40000, 0, 4, 40000, 160000, '2025-01-02 10:53:36'),
(0, '7', 1, 10000, 0, 1, 10000, 10000, '2025-01-02 10:53:36'),
(0, '2', 1, 25000, 0, 5, 25000, 125000, '2025-01-02 10:59:06');

-- --------------------------------------------------------

--
-- Table structure for table `sales_list`
--

CREATE TABLE `sales_list` (
  `id` int(30) NOT NULL,
  `ref_no` varchar(30) NOT NULL,
  `customer_id` int(30) NOT NULL,
  `total_amount` double NOT NULL,
  `amount_tendered` double NOT NULL,
  `amount_change` double NOT NULL,
  `date_updated` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sales_list`
--

INSERT INTO `sales_list` (`id`, `ref_no`, `customer_id`, `total_amount`, `amount_tendered`, `amount_change`, `date_updated`) VALUES
(1, '00000000\r\n', 0, 250, 300, 50, '2020-09-22 15:19:22'),
(2, '17671173\n', 2, 200, 200, 0, '2020-09-22 15:00:46'),
(3, '16042993\n', 2, 100, 1000, 900, '2020-09-22 15:01:55'),
(4, '50470080\n', 0, 1175, 1200, 25, '2020-09-22 15:42:59');

-- --------------------------------------------------------

--
-- Table structure for table `supplier_list`
--

CREATE TABLE `supplier_list` (
  `SupplierID` int(30) NOT NULL,
  `supplier_name` text NOT NULL,
  `contact` varchar(30) NOT NULL,
  `address` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `supplier_list`
--

INSERT INTO `supplier_list` (`SupplierID`, `supplier_name`, `contact`, `address`) VALUES
(3, 'Supplier 2', '0778449169', 'Supplier2 Address'),
(4, 'Kimuli Done', '0778449169', 'Nansana');

-- --------------------------------------------------------

--
-- Table structure for table `system_settings`
--

CREATE TABLE `system_settings` (
  `id` int(30) NOT NULL,
  `name` text NOT NULL,
  `email` varchar(200) NOT NULL,
  `contact` varchar(20) NOT NULL,
  `cover_img` text NOT NULL,
  `about_content` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `system_settings`
--

INSERT INTO `system_settings` (`id`, `name`, `email`, `contact`, `cover_img`, `about_content`) VALUES
(1, 'Online Food Ordering System', 'info@sample.com', '+6948 8542 623', '1600654680_photo-1504674900247-0877df9cc836.jpg', '&lt;p style=&quot;text-align: center; background: transparent; position: relative;&quot;&gt;&lt;span style=&quot;font-size:28px;background: transparent; position: relative;&quot;&gt;ABOUT US&lt;/span&gt;&lt;/b&gt;&lt;/span&gt;&lt;/p&gt;&lt;p style=&quot;text-align: center; background: transparent; position: relative;&quot;&gt;&lt;span style=&quot;background: transparent; position: relative; font-size: 14px;&quot;&gt;&lt;span style=&quot;font-size:28px;background: transparent; position: relative;&quot;&gt;&lt;b style=&quot;margin: 0px; padding: 0px; color: rgb(0, 0, 0); font-family: &amp;quot;Open Sans&amp;quot;, Arial, sans-serif; text-align: justify;&quot;&gt;Lorem Ipsum&lt;/b&gt;&lt;span style=&quot;color: rgb(0, 0, 0); font-family: &amp;quot;Open Sans&amp;quot;, Arial, sans-serif; font-weight: 400; text-align: justify;&quot;&gt;&amp;nbsp;is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry&amp;#x2019;s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.&lt;/span&gt;&lt;br&gt;&lt;/span&gt;&lt;/b&gt;&lt;/span&gt;&lt;/p&gt;&lt;p style=&quot;text-align: center; background: transparent; position: relative;&quot;&gt;&lt;span style=&quot;background: transparent; position: relative; font-size: 14px;&quot;&gt;&lt;span style=&quot;font-size:28px;background: transparent; position: relative;&quot;&gt;&lt;span style=&quot;color: rgb(0, 0, 0); font-family: &amp;quot;Open Sans&amp;quot;, Arial, sans-serif; font-weight: 400; text-align: justify;&quot;&gt;&lt;br&gt;&lt;/span&gt;&lt;/b&gt;&lt;/span&gt;&lt;/p&gt;&lt;p style=&quot;text-align: center; background: transparent; position: relative;&quot;&gt;&lt;span style=&quot;background: transparent; position: relative; font-size: 14px;&quot;&gt;&lt;span style=&quot;font-size:28px;background: transparent; position: relative;&quot;&gt;&lt;h2 style=&quot;font-size:28px;background: transparent; position: relative;&quot;&gt;Where does it come from?&lt;/h2&gt;&lt;p style=&quot;text-align: center; margin-bottom: 15px; padding: 0px; color: rgb(0, 0, 0); font-family: &amp;quot;Open Sans&amp;quot;, Arial, sans-serif; font-weight: 400;&quot;&gt;Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia, looked up one of the more obscure Latin words, consectetur, from a Lorem Ipsum passage, and going through the cites of the word in classical literature, discovered the undoubtable source. Lorem Ipsum comes from sections 1.10.32 and 1.10.33 of &quot;de Finibus Bonorum et Malorum&quot; (The Extremes of Good and Evil) by Cicero, written in 45 BC. This book is a treatise on the theory of ethics, very popular during the Renaissance. The first line of Lorem Ipsum, &quot;Lorem ipsum dolor sit amet..&quot;, comes from a line in section 1.10.32.&lt;/p&gt;&lt;/span&gt;&lt;/b&gt;&lt;/span&gt;&lt;/p&gt;');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('admin','user','moderator','Dean','Head OF Department','School Practice Supervisor') NOT NULL DEFAULT 'user'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `role`) VALUES
(2, 'admin', '1234', 'admin'),
(3, 'isaaya', '1234', 'user');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `category_list`
--
ALTER TABLE `category_list`
  ADD PRIMARY KEY (`CategoryID`);

--
-- Indexes for table `customer_list`
--
ALTER TABLE `customer_list`
  ADD PRIMARY KEY (`CustomerID`);

--
-- Indexes for table `inventory`
--
ALTER TABLE `inventory`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `inventory_logs`
--
ALTER TABLE `inventory_logs`
  ADD PRIMARY KEY (`inventory_log_id`);

--
-- Indexes for table `product_list`
--
ALTER TABLE `product_list`
  ADD PRIMARY KEY (`ProductID`);

--
-- Indexes for table `receiving_list`
--
ALTER TABLE `receiving_list`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `sales_list`
--
ALTER TABLE `sales_list`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `supplier_list`
--
ALTER TABLE `supplier_list`
  ADD PRIMARY KEY (`SupplierID`);

--
-- Indexes for table `system_settings`
--
ALTER TABLE `system_settings`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `category_list`
--
ALTER TABLE `category_list`
  MODIFY `CategoryID` int(30) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `customer_list`
--
ALTER TABLE `customer_list`
  MODIFY `CustomerID` int(30) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `inventory`
--
ALTER TABLE `inventory`
  MODIFY `id` int(30) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `inventory_logs`
--
ALTER TABLE `inventory_logs`
  MODIFY `inventory_log_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- AUTO_INCREMENT for table `product_list`
--
ALTER TABLE `product_list`
  MODIFY `ProductID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `receiving_list`
--
ALTER TABLE `receiving_list`
  MODIFY `id` int(30) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `sales_list`
--
ALTER TABLE `sales_list`
  MODIFY `id` int(30) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `supplier_list`
--
ALTER TABLE `supplier_list`
  MODIFY `SupplierID` int(30) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `system_settings`
--
ALTER TABLE `system_settings`
  MODIFY `id` int(30) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
