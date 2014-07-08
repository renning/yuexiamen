CREATE TABLE `pre_country` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(245) NOT NULL,
  PRIMARY KEY (`id`),
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

CREATE TABLE `pre_province` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `countryid` int(11) NOT NULL,
  `name` varchar(245) NOT NULL,
  `overview` varchar(1000) NOT NULL,
  PRIMARY KEY (`id`),
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

CREATE TABLE `pre_area` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `countryid` int(11) NOT NULL,
  `provinceid` int(11) NOT NULL,
  `name` varchar(245) NOT NULL,
  `overview` varchar(1000) NOT NULL,
  PRIMARY KEY (`id`),
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

CREATE TABLE `pre_city` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `countryid` int(11) NOT NULL,
  `provinceid` int(11) NOT NULL,
  `areaid` int(11) NOT NULL,
  `name` varchar(245) NOT NULL,
  `overview` varchar(1000) NOT NULL,
  PRIMARY KEY (`id`),
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

CREATE TABLE `pre_spot` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `countryid` int(11) NOT NULL,
  `provinceid` int(11) NOT NULL,
  `areaid` int(11) NOT NULL,
  `cityid` int(11) NOT NULL,
  `name` varchar(245) NOT NULL,
  `overview` varchar(1000) NOT NULL,
  `commentsnum` int(11) ,
  `score` int(11) ,
  `address` varchar(500) ,
  PRIMARY KEY (`id`),
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;


CREATE TABLE `pre_spot_comments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `spotid` int(11) NOT NULL,
  `uid` int(11) NOT NULL,
  `content` varchar(1000) NOT NULL,
  `createtime` int(11) ,
  `uptimes` int(11) ,
  PRIMARY KEY (`id`),
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;


CREATE TABLE `pre_specialty` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `areaid` int(11) NOT NULL,
  `name` varchar(245) NOT NULL,
  `commentsnum` int(11) ,
  `score` int(11) ,
  PRIMARY KEY (`id`),
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;


CREATE TABLE `pre_specialty_comments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `specialtyid` int(11) NOT NULL,
  `uid` int(11) NOT NULL,
  `content` varchar(1000) NOT NULL,
  `createtime` int(11) ,
  `uptimes` int(11) ,
  PRIMARY KEY (`id`),
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

####

CREATE TABLE `pre_area` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `countryid` int(11) NOT NULL,
  `provinceid` int(11) NOT NULL,
  `name` varchar(245) NOT NULL,
  `overview` varchar(1000) NOT NULL,
  `mfwid` int(8) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=557 DEFAULT CHARSET=utf8;
CREATE TABLE `pre_country` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(245) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
CREATE TABLE `pre_place` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `area` varchar(245) DEFAULT NULL,
  `areaid` int(11) DEFAULT NULL,
  `name` varchar(45) DEFAULT NULL,
  `placetype` int(2) DEFAULT NULL,
  `address` varchar(245) DEFAULT NULL,
  `phone` int(12) DEFAULT NULL,
  `introduction` text,
  `site` varchar(245) DEFAULT NULL,
  `price` varchar(45) DEFAULT NULL,
  `businesshours` varchar(500) DEFAULT NULL,
  `traffic` text,
  `createtime` int(12) DEFAULT NULL,
  `parentplaceid` int(10) DEFAULT NULL,
  `parentplacename` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;
CREATE TABLE `pre_province` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `countryid` int(11) NOT NULL,
  `name` varchar(245) NOT NULL,
  `overview` varchar(1000) NOT NULL,
  `mfwid` int(8) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8;
CREATE TABLE `pre_poi` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `area` varchar(245) DEFAULT NULL,
  `areaid` int(11) DEFAULT NULL,
  `name` varchar(45) DEFAULT NULL,
  `introduction` text,
  `createtime` int(12) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;

