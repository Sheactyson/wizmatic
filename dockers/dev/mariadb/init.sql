CREATE DATABASE IF NOT EXISTS `wizmatic` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `wizmatic`;
-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: wizmatic
-- ------------------------------------------------------
-- Server version	11.2.3-MariaDB-1:11.2.3+maria~ubu2204

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `card`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `card` (
  `cardID` varchar(45) NOT NULL,
  `cardURL` varchar(100) DEFAULT 'none',
  `cardIMG` varchar(100) DEFAULT 'none',
  `cardNAME` varchar(45) DEFAULT 'none',
  `cardDESC` varchar(300) DEFAULT 'none',
  `cardCATEGORY` varchar(45) DEFAULT 'none',
  `cardTYPE` varchar(100) DEFAULT 'none',
  `cardSCHOOL` varchar(45) DEFAULT 'none',
  `cardREGPIP` int(11) DEFAULT -1,
  `cardSCHPIP` int(11) DEFAULT -1,
  `cardSHDPIP` int(11) DEFAULT -1,
  `cardACC` int(11) DEFAULT -1,
  `cardPIERCE` int(11) DEFAULT -1,
  `cardMINDAM` int(11) DEFAULT -1,
  `cardMAXDAM` int(11) DEFAULT -1,
  `cardHEAL` int(11) DEFAULT -1,
  `cardROUNDS` int(11) DEFAULT -1,
  `cardDOT` int(11) DEFAULT -1,
  `cardHOT` int(11) DEFAULT -1,
  `cardPERCENT` int(11) DEFAULT -1,
  `cardMETA` varchar(100) DEFAULT 'none',
  `cardTARGET1` varchar(45) DEFAULT 'none',
  `cardTARGET2` varchar(45) DEFAULT 'none',
  `cardSPECIAL1` varchar(45) DEFAULT 'none',
  `cardSPECIAL2` varchar(45) DEFAULT 'none',
  `cardSPECIAL3` varchar(45) DEFAULT 'none',
  PRIMARY KEY (`cardID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

GRANT ALL PRIVILEGES ON wizmatic.* TO 'user'@'%' WITH GRANT OPTION;