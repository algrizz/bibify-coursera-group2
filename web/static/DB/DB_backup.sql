-- MySQL dump 10.13  Distrib 5.7.19, for Linux (x86_64)
--
-- Host: localhost    Database: COURSERA
-- ------------------------------------------------------
-- Server version	5.7.19-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `MESSAGEBOARD`
--

DROP TABLE IF EXISTS `MESSAGEBOARD`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `MESSAGEBOARD` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `MSG` varchar(500) NOT NULL,
  `TITLE` varchar(50) NOT NULL,
  `SOURCE` varchar(30) NOT NULL,
  `DESTINATION` varchar(30) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MESSAGEBOARD`
--

LOCK TABLES `MESSAGEBOARD` WRITE;
/*!40000 ALTER TABLE `MESSAGEBOARD` DISABLE KEYS */;
INSERT INTO `MESSAGEBOARD` VALUES (10,'A lacnic desde rocket, message. Ojala sirva; select * from USERS;','A rocket, primero desde Lacnic','aacosta@rocketmail.com','alejandro@lacnic.net'),(11,'veamos que pasa. Ojala sirva. Select * from USERS WHERE 1=1;','A rocket desde Lacnic','alejandro@lacnic.net','aacosta@rocketmail.com');
/*!40000 ALTER TABLE `MESSAGEBOARD` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `SECONDFACTOR`
--

DROP TABLE IF EXISTS `SECONDFACTOR`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `SECONDFACTOR` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `EMAIL` varchar(30) NOT NULL,
  `CODE` varchar(41) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SECONDFACTOR`
--

LOCK TABLES `SECONDFACTOR` WRITE;
/*!40000 ALTER TABLE `SECONDFACTOR` DISABLE KEYS */;
/*!40000 ALTER TABLE `SECONDFACTOR` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `UNVERIFIED_USER`
--

DROP TABLE IF EXISTS `UNVERIFIED_USER`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `UNVERIFIED_USER` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `EMAIL` varchar(30) NOT NULL,
  `CODE` varchar(41) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `UNVERIFIED_USER`
--

LOCK TABLES `UNVERIFIED_USER` WRITE;
/*!40000 ALTER TABLE `UNVERIFIED_USER` DISABLE KEYS */;
/*!40000 ALTER TABLE `UNVERIFIED_USER` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `USERS`
--

DROP TABLE IF EXISTS `USERS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `USERS` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `FULLNAME` varchar(40) NOT NULL,
  `PASS` varchar(100) NOT NULL,
  `EMAIL` varchar(30) NOT NULL,
  `VERIFIED` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `EMAIL` (`EMAIL`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `USERS`
--

LOCK TABLES `USERS` WRITE;
/*!40000 ALTER TABLE `USERS` DISABLE KEYS */;
INSERT INTO `USERS` VALUES (22,'Alejandro Acosta','0428a6b7bdc500d14eeb9242a99b84409ec3afa73f6a689d446479888758f40a080c4f99778f501dd0b37baf233c1556','alejandro@lacnic.net',0),(23,'Alejandro Acosta Rocket','48c12a2bc7968157fa32901082ddf24aec3777ef6369ad4999a06b85a755693cf48ce78bb39e20a4faf0f0dda07a6c89','aacosta@rocketmail.com',0),(24,'Alejandro Acosta GMAIL','2d091ed14c72b24e5b6edca14944615549602c6e9609594bf298b8abcf184d0e7ef007e43aa260cef562b227f6480159','alejandroacostaalamo@gmail.com',0);
/*!40000 ALTER TABLE `USERS` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-09-21 18:15:51
