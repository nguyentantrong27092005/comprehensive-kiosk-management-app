CREATE SCHEMA IF NOT EXISTS `kioskapp`;
CREATE TABLE IF NOT EXISTS `kioskapp`.`evouchergiamgialist` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `EVoucherGiamGiaID` INT NULL,
  `Value` VARCHAR(20) NULL,
  `IsUsed` TINYINT NULL,
  `CreateAt` DATETIME NULL,
  `UpdateAt` DATETIME NULL,
  `DeleteAt` DATETIME NULL,
  PRIMARY KEY (`ID`))
ENGINE = InnoDB;
CREATE TABLE IF NOT EXISTS `kioskapp`.`evouchergiamgia` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `EVoucherID` INT NULL,
  `Discount` INT NULL,
  `IsPercent` TINYINT NULL,
  `MinimumPrice` INT NULL,
  `MaximumDiscount` INT NULL,
  `CreateAt` DATETIME NULL,
  `UpdateAt` DATETIME NULL,
  `DeleteAt` DATETIME NULL,
  PRIMARY KEY (`ID`))
ENGINE = InnoDB;
CREATE TABLE IF NOT EXISTS `kioskapp`.`evoucher` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `Name` VARCHAR(256) NULL,
  `Category` ENUM('Giam gia', 'Tang mon') NULL,
  `ExpiryDate` DATETIME NULL,
  `IsEffective` TINYINT NULL,
  `CreateAt` DATETIME NULL,
  `UpdateAt` DATETIME NULL,
  `DeleteAt` DATETIME NULL,
  PRIMARY KEY (`ID`))
ENGINE = InnoDB;
CREATE TABLE IF NOT EXISTS `kioskapp`.`order` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `EVoucherGiamGiaID` INT NULL,
  `Payment` ENUM('cash', 'bank') NULL,
  `IsDineIn` TINYINT NULL,
  `TotalPrice` INT NULL,
  `TotalAmount` INT NULL,
  `EVoucherDiscount` INT NULL,
  `Status` ENUM('in progress', 'done', 'cancelled') NULL,
  `CreateAt` DATETIME NULL,
  `UpdateAt` DATETIME NULL,
  `DeleteAt` DATETIME NULL,
  PRIMARY KEY (`ID`))
  ENGINE = InnoDB;
CREATE TABLE IF NOT EXISTS `kioskapp`.`orderdetails` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `OrderID` INT NULL,
  `FoodItemID` INT NULL,
  `EVoucherTangMonID` INT NULL,
  `PromotionID` INT NULL,
  `Amount` INT NULL,
  `Price` INT NULL,
  `Discount` INT NULL,
  `Note` TEXT NULL,
  `CreateAt` DATETIME NULL,
  `UpdateAt` DATETIME NULL,
  `DeleteAt` DATETIME NULL,
  PRIMARY KEY (`ID`))
 ENGINE = InnoDB;
CREATE TABLE IF NOT EXISTS `kioskapp`.`evouchertangmonlist` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `EVoucherTangMonID` INT NULL,
  `Value` VARCHAR(20) NULL,
  `IsUsed` TINYINT NULL,
  `CreateAt` DATETIME NULL,
  `UpdateAt` DATETIME NULL,
  `DeleteAt` DATETIME NULL,
  PRIMARY KEY (`ID`))
   ENGINE = InnoDB;
CREATE TABLE IF NOT EXISTS `kioskapp`.`evouchertangmon` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `EVoucherID` INT NULL,
  `FoodItemID` INT NULL,
  `MinimumPrice` INT NULL,
  `CreateAt` DATETIME NULL,
  `UpdateAt` DATETIME NULL,
  `DeleteAt` DATETIME NULL,
  PRIMARY KEY (`ID`))
    ENGINE = InnoDB;
CREATE TABLE IF NOT EXISTS `kioskapp`.`fooditem` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `CategoryID` INT NULL,
  `CustomID` VARCHAR(15) NULL,
  `Name` VARCHAR(256) NULL,
  `IsBestSeller` TINYINT NULL,
  `IsFulltime` TINYINT NULL,
  `Days` VARCHAR(512) NULL,
  `AvailableStartTime` TIME NULL,
  `AvailableEndTime` TIME NULL,
  `ImageURL` VARCHAR(512) NULL,
  `CreateAt` DATETIME NULL,
  `UpdateAt` DATETIME NULL,
  `DeleteAt` DATETIME NULL,
  PRIMARY KEY (`ID`),
  UNIQUE INDEX `CustomID_UNIQUE` (`CustomID` ASC) VISIBLE)
  ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `kioskapp`.`Category` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `Name` VARCHAR(256) NULL,
  `ImageURL` VARCHAR(512) NULL,
  `CreateAt` DATETIME NULL,
  `UpdateAt` DATETIME NULL,
  `DeleteAt` DATETIME NULL,
  PRIMARY KEY (`ID`))
  ENGINE = InnoDB;
CREATE TABLE IF NOT EXISTS `kioskapp`.`toppinggroupfooditem` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `ToppingGroupID` INT NULL,
  `FoodItemID` INT NULL,
  `CreateAt` DATETIME NULL,
  `UpdateAt` DATETIME NULL,
  `DeleteAt` DATETIME NULL,
  PRIMARY KEY (`ID`))
   ENGINE = InnoDB;
CREATE TABLE IF NOT EXISTS `kioskapp`.`variantgroupfooditem` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `VariantGroupID` INT NULL,
  `FoodItemID` INT NULL,
  `CreateAt` DATETIME NULL,
  `UpdateAt` DATETIME NULL,
  `DeleteAt` DATETIME NULL,
  PRIMARY KEY (`ID`))
  ENGINE = InnoDB;
CREATE TABLE IF NOT EXISTS `kioskapp`.`promotionfooditem` (
  `PromotionID` INT NOT NULL,
  `FoodItemID` INT NULL,
  `CreateAt` DATETIME NULL,
  `UpdateAt` DATETIME NULL,
  `DeleteAt` DATETIME NULL)
  ENGINE = InnoDB;
CREATE TABLE IF NOT EXISTS `kioskapp`.`fooditem_history` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `FoodItemID` INT NULL,
  `Price` INT NULL,
  `Cost` INT NULL,
  `IsEffective` TINYINT NULL,
  `CreateAt` DATETIME NULL,
  `UpdateAt` DATETIME NULL,
  `DeleteAt` DATETIME NULL,
  PRIMARY KEY (`ID`))
  ENGINE = InnoDB;
CREATE TABLE IF NOT EXISTS `kioskapp`.`variantgroup` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `Name` VARCHAR(256) NULL,
  `ViewType` VARCHAR(48) NULL,
  `CreateAt` DATETIME NULL,
  `UpdateAt` DATETIME NULL,
  `DeleteAt` DATETIME NULL,
  PRIMARY KEY (`ID`))
  ENGINE = InnoDB;
CREATE TABLE IF NOT EXISTS `kioskapp`.`promotion` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `Name` VARCHAR(256) NULL,
  `Discount` INT NULL,
  `IsPercent` TINYINT NULL,
  `ExpiryDate` DATETIME NULL,
  `IsEffective` TINYINT NULL,
  `CreateAt` DATETIME NULL,
  `UpdateAt` DATETIME NULL,
  `DeleteAt` DATETIME NULL,
  PRIMARY KEY (`ID`))
  ENGINE = InnoDB;
CREATE TABLE IF NOT EXISTS `kioskapp`.`toppinggroup` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `Name` VARCHAR(256) NULL,
  `CreateAt` DATETIME NULL,
  `UpdateAt` DATETIME NULL,
  `DeleteAt` DATETIME NULL,
  PRIMARY KEY (`ID`))
  ENGINE = InnoDB;
CREATE TABLE IF NOT EXISTS `kioskapp`.`topping` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `ToppingGroup` INT NULL,
  `FoodItemID` INT NULL,
  `CreateAt` DATETIME NULL,
  `UpdateAt` DATETIME NULL,
  `DeleteAt` DATETIME NULL,
  PRIMARY KEY (`ID`))
    ENGINE = InnoDB;
CREATE TABLE IF NOT EXISTS `kioskapp`.`orderdetailstopping` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `OrderDetailsID` INT NULL,
  `ToppingID` INT NULL,
  `Price` INT NULL,
  `Discount` INT NULL,
  `CreateAt` DATETIME NULL,
  `UpdateAt` DATETIME NULL,
  `DeleteAt` DATETIME NULL,
  PRIMARY KEY (`ID`))
    ENGINE = InnoDB;
CREATE TABLE IF NOT EXISTS `kioskapp`.`variant` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `VariantGroupID` INT NULL,
  `Value` INT NULL,
  `CreateAt` DATETIME NULL,
  `UpdateAt` DATETIME NULL,
  `DeleteAt` DATETIME NULL,
  PRIMARY KEY (`ID`))
  ENGINE = InnoDB;
CREATE TABLE IF NOT EXISTS `kioskapp`.`user` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `HashingAlgorithmID` INT NULL,
  `Name` VARCHAR(100) NULL,
  `Email` VARCHAR(100) NULL,
  `Username` VARCHAR(20) NULL,
  `PasswordHash` VARCHAR(256) NULL,
  `PasswordSalt` VARCHAR(100) NULL,
  `CreateAt` DATETIME NULL,
  `UpdateAt` DATETIME NULL,
  `DeleteAt` DATETIME NULL,
  PRIMARY KEY (`ID`))
   ENGINE = InnoDB;
CREATE TABLE IF NOT EXISTS `kioskapp`.`hashingalgorithm` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `Name` VARCHAR(10) NULL,
  `CreateAt` DATETIME NULL,
  `UpdateAt` DATETIME NULL,
  `DeleteAt` DATETIME NULL,
  PRIMARY KEY (`ID`))
  ENGINE = InnoDB;