CREATE TABLE `Score_interactions` (
  `Score_Inter_Id` int(11) NOT NULL AUTO_INCREMENT,
  `ProtBactId` varchar(256) DEFAULT NULL,
  `ProtPhageId` varchar(256) DEFAULT NULL,
  `Positiv_Interaction` tinyint(1) DEFAULT NULL,
  `Interaction_Id` int(11) DEFAULT NULL,
  `Score_result` float DEFAULT NULL,
PRIMARY KEY (`Score_Inter_Id`)
);