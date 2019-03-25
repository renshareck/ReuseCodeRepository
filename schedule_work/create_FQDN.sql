CREATE TABLE `FQDN` (
  `ID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `FQDN` varchar(255) NOT NULL,
  `domain` char(128) NOT NULL COMMENT 'FQDN所解析出的域名',
  `malicious_type` varchar(255) NOT NULL DEFAULT '' COMMENT 'FQDN 恶意类型',
  `source` varchar(255) NOT NULL DEFAULT '' COMMENT 'FQDN来源',
  `record_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'FQDN记录插入时间',
  PRIMARY KEY (`ID`),
  UNIQUE KEY `UNI_FQDN` (`FQDN`) USING HASH,
  UNIQUE KEY `UNI_domain` (`domain`) USING HASH,
  KEY `IND_record_time` (`record_time`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=135400118 DEFAULT CHARSET=utf8;