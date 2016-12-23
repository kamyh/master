CREATE TABLE `QtdScores` (
`QS_id` int(11) NOT NULL AUTO_INCREMENT,
`Interaction_Id` int(11) DEFAULT NULL,
`Positiv_Interaction` tinyint(1) DEFAULT NULL,
`ScoreNumber` float DEFAULT NULL,
`QuantityScore` int(11) DEFAULT NULL,
PRIMARY KEY (`QS_id`)
);