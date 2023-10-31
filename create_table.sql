CREATE SCHEMA `sw-arch`;
USE sw-arch;

CREATE TABLE `ventas` (
  `id_cargue` int(11) NOT NULL AUTO_INCREMENT,
  `empresa_local` varchar(20) NOT NULL,
  `valor_venta` int(11) NOT NULL,
  `fecha_venta` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_cargue`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;