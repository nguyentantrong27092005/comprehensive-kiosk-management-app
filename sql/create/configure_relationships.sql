ALTER TABLE `kioskapp`.`evouchergiamgialist`
ADD INDEX `EVoucherGiamGiaID_evouchergiamgialist_idx` (`EVoucherGiamGiaID` ASC) VISIBLE;
;
ALTER TABLE `kioskapp`.`evouchergiamgialist`
ADD CONSTRAINT `EVoucherGiamGiaID_evouchergiamgialist`
  FOREIGN KEY (`EVoucherGiamGiaID`)
  REFERENCES `kioskapp`.`evouchergiamgia` (`ID`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;
ALTER TABLE `kioskapp`.`evouchergiamgia`
ADD INDEX `EVoucherID_evouchergiamgia_idx` (`EVoucherID` ASC) VISIBLE;
;
ALTER TABLE `kioskapp`.`evouchergiamgia`
ADD CONSTRAINT `EVoucherID_evouchergiamgia`
  FOREIGN KEY (`EVoucherID`)
  REFERENCES `kioskapp`.`evoucher` (`ID`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;
ALTER TABLE `kioskapp`.`evouchertangmonlist`
ADD CONSTRAINT `EVoucherTangMonID_evouchertangmonlist`
  FOREIGN KEY (`EVoucherTangMonID`)
  REFERENCES `kioskapp`.`evouchertangmon` (`ID`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;
ALTER TABLE `kioskapp`.`evouchertangmon`
ADD INDEX `FoodItemID_evouchertangmon_idx` (`FoodItemID` ASC) VISIBLE;
;
ALTER TABLE `kioskapp`.`evouchertangmon`
ADD CONSTRAINT `EVoucherID_evouchertangmon`
  FOREIGN KEY (`EVoucherID`)
  REFERENCES `kioskapp`.`evoucher` (`ID`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION,
ADD CONSTRAINT `FoodItemID_evouchertangmon`
  FOREIGN KEY (`FoodItemID`)
  REFERENCES `kioskapp`.`fooditem` (`ID`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;
ALTER TABLE `kioskapp`.`fooditem`
ADD CONSTRAINT `CategoryID_fooditem`
  FOREIGN KEY (`CategoryID`)
  REFERENCES `kioskapp`.`Category` (`ID`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;
ALTER TABLE `kioskapp`.`orderdetails`
ADD CONSTRAINT `OrderID_orderdetails`
  FOREIGN KEY (`OrderID`)
  REFERENCES `kioskapp`.`order` (`ID`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION,
ADD CONSTRAINT `EVoucherTangMonID_orderdetails`
  FOREIGN KEY (`EVoucherTangMonID`)
  REFERENCES `kioskapp`.`evouchertangmon` (`ID`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION,
ADD CONSTRAINT `PromotionID_orderdetails`
  FOREIGN KEY (`PromotionID`)
  REFERENCES `kioskapp`.`promotion` (`ID`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION,
ADD CONSTRAINT `FoodItemID_orderdetails`
  FOREIGN KEY (`FoodItemID`)
  REFERENCES `kioskapp`.`fooditem` (`ID`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;
ALTER TABLE `kioskapp`.`toppinggroupfooditem`
ADD CONSTRAINT `ToppingGroupID_toppinggroupfooditem`
  FOREIGN KEY (`ToppingGroupID`)
  REFERENCES `kioskapp`.`toppinggroup` (`ID`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION,
ADD CONSTRAINT `FoodItemID_toppinggroupfooditem`
  FOREIGN KEY (`FoodItemID`)
  REFERENCES `kioskapp`.`fooditem` (`ID`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;
ALTER TABLE `kioskapp`.`variantgroupfooditem`
ADD CONSTRAINT `VariantGroupID_variantgroupfooditem`
  FOREIGN KEY (`VariantGroupID`)
  REFERENCES `kioskapp`.`toppinggroup` (`ID`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION,
ADD CONSTRAINT `FoodItemID_variantgroupfooditem`
  FOREIGN KEY (`FoodItemID`)
  REFERENCES `kioskapp`.`fooditem` (`ID`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;
ALTER TABLE `kioskapp`.`promotionfooditem`
ADD CONSTRAINT `PromotionID_promotionfooditem`
  FOREIGN KEY (`PromotionID`)
  REFERENCES `kioskapp`.`toppinggroup` (`ID`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION,
ADD CONSTRAINT `FoodItemID_promotionfooditem`
  FOREIGN KEY (`FoodItemID`)
  REFERENCES `kioskapp`.`fooditem` (`ID`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;
ALTER TABLE `kioskapp`.`fooditem_history`
ADD CONSTRAINT `FoodItemID_fooditem_history`
  FOREIGN KEY (`FoodItemID`)
  REFERENCES `kioskapp`.`fooditem` (`ID`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;
ALTER TABLE `kioskapp`.`variant`
ADD CONSTRAINT `VariantGroupID_variant`
  FOREIGN KEY (`VariantGroupID`)
  REFERENCES `kioskapp`.`variant` (`ID`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;
ALTER TABLE `kioskapp`.`topping`
ADD CONSTRAINT `ToppingGroup_topping`
  FOREIGN KEY (`ToppingGroup`)
  REFERENCES `kioskapp`.`toppinggroup` (`ID`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;
ALTER TABLE `kioskapp`.`user`
ADD CONSTRAINT `HashingAlgorithmID_user`
  FOREIGN KEY (`HashingAlgorithmID`)
  REFERENCES `kioskapp`.`hashingalgorithm` (`ID`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;
ALTER TABLE `kioskapp`.`order`
ADD CONSTRAINT `EVoucherGiamGiaID_order`
  FOREIGN KEY (`EVoucherGiamGiaID`)
  REFERENCES `kioskapp`.`evouchergiamgia` (`ID`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;
