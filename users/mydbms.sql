DROP table TBL_STOCK;
create table TBL_STOCK(

Product_ID varchar(2),
Product_Name varchar(20),
Quantity_on_hand Number,
Product_Unit_Price Number,
Reoder_Level Number,

CONSTRAINT pk00 primary key(product_id),
CONSTRAINT uq01 unique(product_name),
CONSTRAINT ch01 check(qunatity_on_hand >= 0),
CONSTRAINT ch002 check(reorder_level >= 0),



);
DROP table TBL_SALES;
create table TBL_SALES(

Sales_Id varchar(6),
Sales_Date Date,
Product_Id varchar(6),
Quantity_Sold Number,
Sales_Price_Per_Unit Number,

CONSTRAINT pk10 primary key(Sales_Id),
CONSTRAINT fk11 foreign key(Producy_Id) REFERENCES TBL_STOCK(Product_Id),
CONSTRAINT ch12 Check(Quantity_Id >= 0),
CONStRAINT ch13 check(Sales_Price_Per_Unit(sales_price_per_unit >=0),

);

INSERT INTO TBL_sTOCK VALUES('RE1001' 'Redmi Note 3' 20, 12000, 5);
INSERT INTO TBL_sTOCK VALUES('IP1002' 'Iphone 5S' 10, 21000, 2);
INSERT INTO TBL_sTOCK VALUES('PS1005' 'Panasonic' 50, 5500, 5);

drop sequence seq_sales_id;
drop sequence seq_product_id;
create sequence seq_sales_id start with 1000 increment by 1;
create sequence seq_product_id start with 100 increment by 1;

drop view v_sales_report;
create view v_sales_report as 
select Sales_Id, Sales_Date, product_id, product_name, Quantity_Sold, Product_Unit_Price, sales_price_per_unit,
                                                (sales_price_per_unit-Product_Unit_Price) Profit_Amount
                        FROM TBL_STOCK NATURAL JOIN TBL_SALES
                        ORDER BY Profit_Amount DESC, Sales_Id ASC;
                                                                    

