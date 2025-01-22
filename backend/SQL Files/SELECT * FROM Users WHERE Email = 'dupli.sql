SELECT * FROM Users WHERE Email = 'duplicate@example.com';
SELECT Password FROM Users WHERE Email = 'duplicate@example.com';


UPDATE Users
SET Password = 'password123'
WHERE Email = 'duplicate@example.com';



DELETE FROM USERS;
COMMIT;


INSERT INTO USERS (USERID, NAME, EMAIL, PHONE, PASSWORD, CURRENCY) VALUES (44, 'Abdullah Salih Ozguven', 'aso@gmail.com', '150200210', 'salihpassword', 'TL');
INSERT INTO USERS (USERID, NAME, EMAIL, PHONE, PASSWORD, CURRENCY) VALUES (45, 'Ata Gunaydin', 'ag@gmail.com', '150210208', 'atapassword', 'TL');
INSERT INTO USERS (USERID, NAME, EMAIL, PHONE, PASSWORD, CURRENCY) VALUES (46, 'Korel Boran Ekici', 'kbe@gmail.com', '150210212', 'korelpassword', 'TL');
COMMIT;


SELECT * FROM USERS;


INSERT INTO USERS (USERID, NAME, EMAIL, PHONE, PASSWORD, CURRENCY) VALUES (46, 'Korel Boran Ekici', 'kbe@gmail.com', '150210212', 'korelpassword', 'TL');
