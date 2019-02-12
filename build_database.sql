USE `badgesdb` ;


CREATE TABLE IF NOT EXISTS Users (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` INT(11) NOT NULL,
  `e_mail` INT(11) NOT NULL,
  `password` INT(11) NOT NULL,
  PRIMARY KEY (`id`));


CREATE TABLE IF NOT EXISTS Badges (
  `id` INT(11) NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `description` VARCHAR(255) NOT NULL,
  `image` MEDIUMBLOB NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC));


CREATE TABLE IF NOT EXISTS Events (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `description` VARCHAR(255) NOT NULL,
  `active` TINYINT NOT NULL,
  `pin` INT(30) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  UNIQUE INDEX `pin_UNIQUE` (`pin` ASC));


CREATE TABLE IF NOT EXISTS EventBadges (
  `badge_id` INT NOT NULL,
  `event_id` INT NOT NULL,
  PRIMARY KEY (`badge_id`, `event_id`),
  CONSTRAINT `FK_EventBadges_Badges`
    FOREIGN KEY (`badge_id`)
    REFERENCES Badges (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_EventBadges_Events`
    FOREIGN KEY (`event_id`)
    REFERENCES Events (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


CREATE TABLE IF NOT EXISTS UserBadges (
  `user_id` INT(11) NOT NULL,
  `badge_id` INT NOT NULL,
  `date` DATETIME(3) NOT NULL,
  PRIMARY KEY (`user_id`, `badge_id`),
  CONSTRAINT `FK_UserBadges_Users`
    FOREIGN KEY (`user_id`)
    REFERENCES Users (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_UserBadges_Badges`
    FOREIGN KEY (`badge_id`)
    REFERENCES Badges (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


CREATE TABLE IF NOT EXISTS Attendees (
  `user_id` INT NOT NULL,
  `event_id` INT NOT NULL,
  PRIMARY KEY (`user_id`, `event_id`),
  CONSTRAINT `fk_Attendees_Users`
    FOREIGN KEY (`user_id`)
    REFERENCES Users (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Attendees_Events`
    FOREIGN KEY (`event_id`)
    REFERENCES Events (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);