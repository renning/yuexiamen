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

