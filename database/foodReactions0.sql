CREATE TABLE ReactionsTypes (
    ID INTEGER NOT NULL,
    ReactionTypeName VARCHAR(150) NOT NULL,
    PRIMARY KEY (ID)
);

CREATE TABLE Reactions (
    ID INTEGER NOT NULL,
    ReactionTypeID INTEGER NOT NULL,
    FoodReactionID INTEGER NOT NULL,
    PRIMARY KEY (ID),
    FOREIGN KEY (ReactionTypeID) REFERENCES ReactionsTypes (ID),
    FOREIGN KEY (FoodReactionID) REFERENCES FoodReactions (ID)
);

CREATE TABLE OutcomesTypes (
    ID INTEGER NOT NULL,
    OutcomeTypeName VARCHAR(150) NOT NULL,
    PRIMARY KEY (ID)
);

CREATE TABLE Outcomes (
    ID INTEGER NOT NULL,
    OutcomesTypeID INTEGER NOT NULL,
    FoodReactionID INTEGER NOT NULL,
    PRIMARY KEY (ID),
    FOREIGN KEY (OutcomesTypeID) REFERENCES OutcomesTypes (ID),
    FOREIGN KEY (FoodReactionID) REFERENCES FoodReactions (ID)
);

CREATE TABLE Products (
    ID INTEGER NOT NULL,
    IndustryNameID INTEGER NOT NULL,
    BrandID INTEGER NOT NULL,
    RoleID INTEGER NOT NULL,
    FoodReactionID INTEGER NOT NULL,
    PRIMARY KEY (ID),
    FOREIGN KEY (IndustryNameID) REFERENCES IndustryNames (ID),
    FOREIGN KEY (BrandID) REFERENCES Brands (ID),
    FOREIGN KEY (RoleID) REFERENCES Roles (ID),
    FOREIGN KEY (FoodReactionID) REFERENCES FoodReactions (ID)
);

CREATE TABLE FoodReactions (
    ID INTEGER NOT NULL,
    ReportNumber VARCHAR(25) NOT NULL,
    DateCreated DATE NOT NULL,
    DateStarted DATE NOT NULL,
    consumerID INTEGER NOT NULL,
    PRIMARY KEY (ID, ReportNumber),
    FOREIGN KEY (consumerID) REFERENCES Consumers (ID)
);

CREATE TABLE Consumers (
    ID INTEGER NOT NULL,
    Age INTEGER NOT NULL,
    AgeUnit VARCHAR(20) NOT NULL,
    Gender VARCHAR(10) NOT NULL,
    PRIMARY KEY (ID)
);

CREATE TABLE IndustryNames (
    ID INTEGER NOT NULL,
    IndustryCode INTEGER NOT NULL,
    IndustryName VARCHAR(100) NOT NULL,
    PRIMARY KEY (ID)
);

CREATE TABLE Brands (
    ID INTEGER NOT NULL,
    BrandName VARCHAR(150) NOT NULL,
    PRIMARY KEY (ID)
);

CREATE TABLE Roles (
    ID INTEGER NOT NULL,
    RoleName VARCHAR(100) NOT NULL,
    PRIMARY KEY (ID)
);
