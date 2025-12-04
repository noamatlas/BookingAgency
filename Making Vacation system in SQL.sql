--Making Vacation system in SQL 26.11.25
----------------------------------------

/*
Vacations:
id, title, destination, startDate, endDate, price, description, availablePlaces, images[], agentId, createdAt, updatedAt

Purchases:
id, vacationId, buyerName, buyerEmail, amount, purchaseDate, agentId

Users:
id, name, email, password, role
*/

USE Vacations
GO

CREATE TABLE Vacations (
	id int IDENTITY(1, 1) PRIMARY KEY NOT NULL,
	title nvarchar(80) NOT NULL,
	destination nvarchar(80) NOT NULL,
	startDate datetime NOT NULL,
	endDate datetime NOT NULL,
	price money NOT NULL,
	fullDescription nvarchar(MAX) NULL,
	availablePlaces nvarchar(MAX) NULL,
	imagesPaths nvarchar(MAX) NULL,
	agentId int NULL,
	createdAt datetime DEFAULT (GETDATE()) NOT NULL,
	updatedAt datetime NULL
)
GO

CREATE TABLE Users (
	id int IDENTITY(1, 1) PRIMARY KEY NOT NULL,
	userName nvarchar(25) NOT NULL,
	email varchar(50) NOT NULL,
	userPassword varchar(50) NOT NULL,
	userRole varchar(25) NOT NULL,
	CONSTRAINT CHK_userRoles CHECK (userRole IN('customer', 'agent'))
)
GO

CREATE TABLE Purchases (
	id int IDENTITY(1, 1) PRIMARY KEY NOT NULL,
	vacationId int NOT NULL,
	customerId int NOT NULL,
	agentId int NOT NULL,
	amount money NOT NULL,
	purchaseDate datetime DEFAULT (GETDATE()) NOT NULL,
	CONSTRAINT FK_Purchases_Vacations FOREIGN KEY (vacationId) REFERENCES Vacations (id),
	CONSTRAINT FK_Purchases_Users_customer FOREIGN KEY (customerId) REFERENCES Users (id),
	CONSTRAINT FK_Purchases_Users_agent FOREIGN KEY (agentId) REFERENCES Users (id)
)
GO


--AI Sample data:
INSERT INTO Users (userName, email, userPassword, userRole)
VALUES
-- Customers
('alice',   'alice@example.com',   'pass123', 'customer'),
('bob',     'bob@example.com',     'pass123', 'customer'),
('charlie', 'charlie@example.com', 'pass123', 'customer'),

-- Agents
('agent_anna', 'anna@travelco.com',  'pass123', 'agent'),
('agent_mike', 'mike@travelco.com',  'pass123', 'agent'),
('agent_sara', 'sara@travelco.com',  'pass123', 'agent')
GO

INSERT INTO Vacations
(title, destination, startDate, endDate, price, fullDescription, availablePlaces, imagesPaths, agentId)
VALUES
('Sunny Beach Escape', 'Spain', '2025-06-10', '2025-06-17', 850, 'A relaxing beach holiday.', '30', '/img/spain1.jpg', 4),
('Mountain Adventure', 'Switzerland', '2025-07-01', '2025-07-08', 1200, 'Hiking and fresh air.', '20', '/img/swiss1.jpg', 4),
('City Lights Tour', 'New York', '2025-05-15', '2025-05-22', 1350, 'Explore NYC attractions.', '25', '/img/ny1.jpg', 5),
('Desert Safari', 'Morocco', '2025-09-05', '2025-09-12', 900, 'Camel tours and dunes.', '18', '/img/morocco1.jpg', 5),
('Tropical Paradise', 'Thailand', '2025-11-01', '2025-11-10', 1100, 'Exotic islands and beaches.', '22', '/img/thai1.jpg', 6),
('Historic Europe', 'Italy', '2025-04-10', '2025-04-17', 950, 'Culture, food, and history.', '27', '/img/italy1.jpg', 4),
('Safari Expedition', 'Kenya', '2025-08-12', '2025-08-20', 2100, 'Wildlife and nature.', '15', '/img/kenya1.jpg', 5),
('Nordic Escape', 'Iceland', '2025-12-01', '2025-12-08', 1700, 'Glaciers and lagoons.', '12', '/img/iceland1.jpg', 6),
('Island Hopper', 'Greece', '2025-06-20', '2025-06-27', 750, 'Sea, sun, and tavernas.', '40', '/img/greece1.jpg', 4),
('Rainforest Journey', 'Costa Rica', '2025-10-01', '2025-10-10', 1600, 'Rainforests and wildlife.', '14', '/img/cr1.jpg', 5),
('Cultural India', 'India', '2025-02-10', '2025-02-20', 1300, 'Rich culture and cuisine.', '19', '/img/india1.jpg', 6),
('Ski Getaway', 'Austria', '2025-01-15', '2025-01-22', 1400, 'Ski slopes and apres-ski.', '17', '/img/austria1.jpg', 4)
GO

INSERT INTO Purchases (vacationId, customerId, agentId, amount)
VALUES
(1, 1, 4, 850),
(3, 2, 5, 1350),
(5, 3, 6, 1100),
(7, 1, 5, 2100),
(9, 2, 4, 750)
GO

SELECT * FROM Users
SELECT * FROM Vacations
SELECT * FROM Purchases

SELECT DISTINCT destination AS Countries FROM Vacations
SELECT * FROM Vacations WHERE destination LIKE 'greece%' ORDER BY startDate
