/*Khi khách bấm vào nút gửi, em sẽ cập nhật lại vào db như sau:*/
UPDATE order
SET CustomerVote = {Số sao khách hàng chọn}
AND ReasonVote = {Lý do vote của khách hàng, nếu chọn nhiều lý do thì viêt dính vào vào được ngăn cách bởi dấu “|”. VD: Chất lượng phục vụ kém|Thời gian chờ đợi lâu}
WHERE ID = {OrderID lấy từ màn hình thanh toán}
--Nếu khách không bấm nút gửi thì không thực hiện gì thêm.
