IF DB_ID(N'RetailAnalytics') IS NULL
    CREATE DATABASE RetailAnalytics;
GO

USE RetailAnalytics;
GO

IF OBJECT_ID(N'dbo.MasterTransactions', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.MasterTransactions (
        Transaction_ID     NVARCHAR(50) NOT NULL PRIMARY KEY,
        Transaction_Date   DATETIME2(0) NOT NULL,
        Customer_ID        NVARCHAR(50) NOT NULL,
        Gender             NVARCHAR(30) NOT NULL,
        Age                INT NOT NULL,
        City               NVARCHAR(200) NOT NULL,
        Product_ID         BIGINT NOT NULL,
        Product_Name       NVARCHAR(MAX) NOT NULL,
        Category           NVARCHAR(255) NOT NULL,
        Brand              NVARCHAR(255) NOT NULL,
        Quantity           INT NOT NULL,
        Unit_Price_VND     DECIMAL(28, 4) NOT NULL,
        Revenue            DECIMAL(28, 4) NOT NULL,
        Source_Currency    NVARCHAR(20) NOT NULL,
        Rating             INT NOT NULL,
        Customer_Review    NVARCHAR(MAX) NOT NULL,

        Original_Price     DECIMAL(28, 8) NULL,
        Discount_Price     DECIMAL(28, 8) NULL,
        Original_Price_VND DECIMAL(28, 4) NULL,
        Discount_Price_VND DECIMAL(28, 4) NULL,

        avg_rating         NVARCHAR(100) NULL,
        reviews_count      NVARCHAR(100) NULL,
        rating_average     DECIMAL(12, 6) NULL,
        review_count       DECIMAL(20, 4) NULL,
        quantity_sold      DECIMAL(20, 4) NULL,
        availability       NVARCHAR(100) NULL,
        is_for_sale        NVARCHAR(100) NULL,
        description        NVARCHAR(MAX) NULL,
        product_type       NVARCHAR(255) NULL,
        category_2         NVARCHAR(255) NULL,
        category_3         NVARCHAR(255) NULL,
        manufacturer       NVARCHAR(255) NULL,
        current_seller     NVARCHAR(255) NULL,
        fulfillment_type   NVARCHAR(255) NULL,
        date_created       NVARCHAR(100) NULL,
        number_of_images   DECIMAL(20, 4) NULL,
        favourite_count    DECIMAL(20, 4) NULL,
        has_video          NVARCHAR(100) NULL,
        Source             NVARCHAR(100) NOT NULL
    );
END;
GO