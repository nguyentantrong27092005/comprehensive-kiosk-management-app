CREATE SCHEMA `kioskapp`;
CREATE TABLE `kioskapp`.`evouchergiamgialist` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `EVoucherGiamGiaID` INT NULL,
  `Value` VARCHAR(20) NULL,
  `IsUsed` TINYINT NULL,
  PRIMARY KEY (`ID`))
ENGINE = InnoDB;
CREATE TABLE `kioskapp`.`evouchergiamgia` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `EVoucherID` INT NULL,
  `Discount` INT NULL,
  `IsPercent` TINYINT NULL,
  `ExpiryDate` DATETIME NULL,
  `IsEffective` TINYINT NULL,
  PRIMARY KEY (`ID`))
ENGINE = InnoDB;
CREATE TABLE `kioskapp`.`evoucher` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `Name` VARCHAR(256) NULL,
  `Category` ENUM('Giam gia', 'Tang mon') NULL,
  `ExpiryDate` DATETIME NULL,
  `IsEffective` TINYINT NULL,
  PRIMARY KEY (`ID`))
ENGINE = InnoDB;
CREATE TABLE `kioskapp`.`order` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `EVoucherGiamGiaID` INT NULL,
  `Payment` ENUM('cash', 'bank') NULL,
  `IsDineIn` TINYINT NULL,
  `TotalPrice` INT NULL,
  `TotalAmount` INT NULL,
  `EVoucherDiscount` INT NULL,
  `Status` ENUM('in progress', 'done', 'cancelled') NULL,
  PRIMARY KEY (`ID`))
  ENGINE = InnoDB;
CREATE TABLE `kioskapp`.`orderdetails` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `OrderID` INT NULL,
  `FoodItemID` INT NULL,
  `EVoucherTangMonID` INT NULL,
  `PromotionID` INT NULL,
  `Amount` INT NULL,
  `Price` INT NULL,
  `Discount` INT NULL,
  `Note` TEXT NULL,
  PRIMARY KEY (`ID`))
 ENGINE = InnoDB;
CREATE TABLE `kioskapp`.`evouchertangmonlist` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `EVoucherTangMonID` INT NULL,
  `Value` VARCHAR(20) NULL,
  `IsUsed` TINYINT NULL,
  PRIMARY KEY (`ID`))
   ENGINE = InnoDB;
CREATE TABLE `kioskapp`.`evouchertangmon` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `EVoucherID` INT NULL,
  `FoodItemID` INT NULL,
  `ExpiryDate` DATETIME NULL,
  `IsEffective` TINYINT NULL,
  PRIMARY KEY (`ID`))
    ENGINE = InnoDB;
CREATE TABLE `kioskapp`.`fooditem` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `CategoryID` INT NULL,
  `CustomID` VARCHAR(15) NULL,
  `Name` VARCHAR(256) NULL,
  `IsBestSeller` TINYINT NULL,
  `IsFulltime` TINYINT NULL,
  `Time` VARCHAR(512) NULL,
  PRIMARY KEY (`ID`),
  UNIQUE INDEX `CustomID_UNIQUE` (`CustomID` ASC) VISIBLE)
  ENGINE = InnoDB;

CREATE TABLE `kioskapp`.`Category` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `Name` VARCHAR(256) NULL,
  PRIMARY KEY (`ID`))
  ENGINE = InnoDB;
CREATE TABLE `kioskapp`.`toppinggroupfooditem` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `ToppingGroupID` INT NULL,
  `FoodItemID` INT NULL,
  PRIMARY KEY (`ID`))
   ENGINE = InnoDB;
CREATE TABLE `kioskapp`.`variantgroupfooditem` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `VariantGroupID` INT NULL,
  `FoodItemID` INT NULL,
  PRIMARY KEY (`ID`))
  ENGINE = InnoDB;
CREATE TABLE `kioskapp`.`promotionfooditem` (
  `PromotionID` INT NOT NULL,
  `FoodItemID` INT NULL)
  ENGINE = InnoDB;
CREATE TABLE `kioskapp`.`fooditem_history` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `FoodItemID` INT NULL,
  `Price` INT NULL,
  `Cost` INT NULL,
  `IsEffective` TINYINT NULL,
  PRIMARY KEY (`ID`))
  ENGINE = InnoDB;
CREATE TABLE `kioskapp`.`variantgroup` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `Name` VARCHAR(256) NULL,
  `IsMultipleSelect` TINYINT NULL,
  `IsRequired` TINYINT NULL,
  `IsSlider` TINYINT NULL,
  PRIMARY KEY (`ID`))
  ENGINE = InnoDB;
CREATE TABLE `kioskapp`.`promotion` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `Name` VARCHAR(256) NULL,
  `Discount` INT NULL,
  `IsPercent` TINYINT NULL,
  `ExpiryDate` DATETIME NULL,
  `IsEffective` TINYINT NULL,
  PRIMARY KEY (`ID`))
  ENGINE = InnoDB;
CREATE TABLE `kioskapp`.`toppinggroup` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `Name` VARCHAR(256) NULL,
  PRIMARY KEY (`ID`))
  ENGINE = InnoDB;
CREATE TABLE `kioskapp`.`topping` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `ToppingGroup` INT NULL,
  `Name` VARCHAR(256) NULL,
  `Price` INT NULL,
  `Cost` INT NULL,
  PRIMARY KEY (`ID`))
    ENGINE = InnoDB;
CREATE TABLE `kioskapp`.`variant` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `VariantGroupID` INT NULL,
  `Value` INT NULL,
  PRIMARY KEY (`ID`))
  ENGINE = InnoDB;
CREATE TABLE `kioskapp`.`user` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `HashingAlgorithmID` INT NULL,
  `Name` VARCHAR(100) NULL,
  `Email` VARCHAR(100) NULL,
  `Username` VARCHAR(20) NULL,
  `PasswordHash` VARCHAR(256) NULL,
  `PasswordSalt` VARCHAR(100) NULL,
  PRIMARY KEY (`ID`))
   ENGINE = InnoDB;
CREATE TABLE `kioskapp`.`hashingalgorithm` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `Name` VARCHAR(10) NULL,
  PRIMARY KEY (`ID`))
  ENGINE = InnoDB;