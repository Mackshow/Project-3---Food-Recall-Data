

CREATE TABLE "Reactions" (
    "ReportNumber" VARCHAR(25) NOT NULL,
    "Reactions" VARCHAR(500) NOT NULL,
    FOREIGN KEY ("ReportNumber") REFERENCES "FoodReactions" ("ReportNumber")
);

CREATE TABLE "Consumer" (
    "ReportNumber" VARCHAR(25) NOT NULL,
    "Age" INTEGER NOT NULL,
    "AgeUnit" VARCHAR(20) NOT NULL,
    "Gender" VARCHAR(20) NOT NULL,
    FOREIGN KEY ("ReportNumber") REFERENCES "FoodReactions" ("ReportNumber")
);

CREATE TABLE "Products" (
    "ReportNumber" VARCHAR(25) NOT NULL,
    "Role" VARCHAR(50) NOT NULL,
    "NameBrand" VARCHAR(255) NOT NULL,
    "IndustryCode" INTEGER NOT NULL,
    "IndusteryName" VARCHAR(255) NOT NULL,
    FOREIGN KEY ("ReportNumber") REFERENCES "FoodReactions" ("ReportNumber")
);

CREATE TABLE "Outcomes" (
    "ReportNumber" VARCHAR(25) NOT NULL,
    "Outcome" VARCHAR(150) NOT NULL,
    FOREIGN KEY ("ReportNumber") REFERENCES "FoodReactions" ("ReportNumber")
);

CREATE TABLE "FoodReactions" (
    "ReportNumber" VARCHAR(25) NOT NULL,
    "DateCreated" DATE NOT NULL,
    "DateStarted" DATE NOT NULL,
    PRIMARY KEY ("ReportNumber")
);
