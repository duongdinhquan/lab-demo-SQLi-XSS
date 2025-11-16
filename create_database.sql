-- 1. Tạo và chọn Database
CREATE DATABASE IF NOT EXISTS quan_ly_sinh_vien
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE quan_ly_sinh_vien;

-- 2. Tạo bảng 'log_in' (Bảng cha)
-- (Đã đổi tên từ 'login' thành 'log_in' theo yêu cầu của bạn)
CREATE TABLE log_in (
    msv VARCHAR(20) PRIMARY KEY,
    passwd VARCHAR(255) NOT NULL,
    role INT NOT NULL -- 0 cho user, 1 cho admin
) ENGINE=InnoDB;

-- 3. Tạo bảng 'user' (Con 1-1 của 'log_in')
CREATE TABLE user (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    msv VARCHAR(20) NOT NULL UNIQUE, -- UNIQUE để đảm bảo quan hệ 1-1
    hoten VARCHAR(100),
    avatar VARCHAR(255),
    gpa DECIMAL(3, 2),
    
    CONSTRAINT fk_user_login 
        FOREIGN KEY (msv) 
        REFERENCES log_in(msv)
        ON DELETE CASCADE -- Tự động xóa user nếu log_in bị xóa
) ENGINE=InnoDB;

-- 4. Tạo bảng 'comment' (Con 1-N của 'log_in')
CREATE TABLE comment (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    msv VARCHAR(20) NOT NULL,
    cmt TEXT,
    
    CONSTRAINT fk_comment_login 
        FOREIGN KEY (msv) 
        REFERENCES log_in(msv)
        ON DELETE CASCADE -- Tự động xóa comment nếu log_in bị xóa
) ENGINE=InnoDB;

-- 5. Chèn 3 bản ghi vào 'log_in'
-- (1 admin role=1, 2 user role=0)
INSERT INTO log_in (msv, passwd, role) VALUES
('admin_main', '1234', 1),
('sv001', '1111', 0),
('sv002', '1111', 0);

-- 6. Chèn 3 bản ghi vào 'user' (tương ứng với 'log_in')
INSERT INTO user (msv, hoten, avatar, gpa) VALUES
('admin_main', 'Quản Trị Viên', 'avatars/admin.png', 0.00),
('sv001', 'Nguyễn Văn Hùng', 'avatars/sv001.png', 3.15),
('sv002', 'Lê Thị An', 'avatars/sv002.png', 2.90);

-- 7. Chèn 3 bản ghi vào 'comment'
INSERT INTO comment (msv, cmt) VALUES
('sv001', 'Xin chào, trang web rất hay!'),
('sv002', 'Mình muốn hỏi về lịch học.'),
('sv001', 'Làm sao để cập nhật ảnh đại diện?');

-- Hoàn tất!