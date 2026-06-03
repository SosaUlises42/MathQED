-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         10.4.32-MariaDB
-- SO del servidor:              Win64
-- HeidiSQL Versión:             12.6.0.6765
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Volcando estructura de base de datos para mathqed
CREATE DATABASE IF NOT EXISTS `mathqed` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `mathqed`;

-- Volcando estructura para tabla mathqed.user
CREATE TABLE IF NOT EXISTS `user` (
  `Usuario_ID` int(11) NOT NULL AUTO_INCREMENT,
  `Nombre` varchar(100) NOT NULL,
  `Correo` varchar(255) NOT NULL,
  `NumeroCRTL` varchar(14) NOT NULL,
  `Password_Hash` varchar(255) NOT NULL,
  `Grado` varchar(1) NOT NULL,
  `Grupo` varchar(1) NOT NULL,
  PRIMARY KEY (`Usuario_ID`),
  UNIQUE KEY `Correo_Unico` (`Correo`),
  UNIQUE KEY `NumCtrl_Unico` (`NumeroCRTL`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT IGNORE INTO `user` (`Nombre`, `Correo`, `NumeroCRTL`, `Password_Hash`, `Grado`, `Grupo`) 
VALUES ('Sosa', 'parafc2026@gmail.com', '23308060610395', '$2b$12$XA4.6iYUtLz3yKBMgcMOF.RQY5MsZ8KrsQGkx6ft7Pp0btKZ//x0W', '6', 'D');

-- Volcando estructura para tabla mathqed.historial
CREATE TABLE IF NOT EXISTS `historial` (
  `id_Consulta` int(11) NOT NULL AUTO_INCREMENT,
  `Ejercicio` varchar(255) NOT NULL,
  `Resultado` text NOT NULL,
  `Favorito` tinyint(1) NOT NULL DEFAULT 0,
  `Usuario_ID` int(11) NOT NULL,
  PRIMARY KEY (`id_Consulta`),
  KEY `Usuario_ID` (`Usuario_ID`),
  CONSTRAINT `historial_ibfk_1` FOREIGN KEY (`Usuario_ID`) REFERENCES `user` (`Usuario_ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;