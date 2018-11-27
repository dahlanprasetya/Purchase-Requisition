DROP DATABASE pr_makers;
CREATE DATABASE pr_makers;
DELETE from material;
SELECT * from kelas;

-- View data
select * from public.position;
select * from public.employee;
select * from public.material;
select * from request;
select * from items;
select * from tweet;

-- add data to position
insert into position(name) values ('Owner');
insert into position(name) values ('Manager');
insert into position(name) values ('SCM');
insert into position(name) values ('Employee');

-- add data to employee

INSERT INTO  public.employee(fullname,email,password,position,photoprofile,payroll_number,token,company,plant) VALUES ('Jhon Pantau','ahaydeuh69@gmail.com','seblak99',4,'https://cdn.idntimes.com/content-images/post/20170816/20399049-1947030192252857-366213070848000000-n-e5b1de42acf427b1a73b795f839388fe_600x400.jpg','72983927','W3yWl9q6blKwp7j5Pd2N2RwzXQ3It-rsY5teyKh7sNU.vN6xrH8UZO1_NMPfDJX7scvJA30TxVzByxvbISbpUos','good company','good plant');
INSERT INTO  public.employee(fullname,email,password,position,photoprofile,payroll_number,token,company,plant) VALUES ('Robert Tantular','oka.aryanata9@gmail.com','seblak99',3,'https://banner2.kisspng.com/20180824/hfj/kisspng-portable-network-graphics-businessperson-jpeg-wind-resume-writing-services-canberra-rev-up-your-resu-5b7fd44917e9f0.179883131535104073098.jpg','72983939','wWU1JDuFglKqbtaidu2CZudJwry61P8Zx3BXcpU3mko.RA3KhZ5VYpPyw7RaU_DSsK0YudAQSl-nAyS-RuB5tgA','good company','good plant');
INSERT INTO  public.employee(fullname,email,password,position,photoprofile,payroll_number,token,company,plant) VALUES ('Asep Junaidi','okaaryanata@gmail.com','seblak99',2,'https://i1.wp.com/www.jabarsatu.com/wp-content/uploads/2014/12/gayus.jpg?fit=311%2C310&ssl=1','43983934','CVfCCBqq0Y8nmMVb5kc5k9rLj4ppPtoKF9TbQJnY74E.qNK0LJQS4KavSCtxSR1fqM4m8vlpI3pPXPt5XZlT5uM','good company','good plant');
INSERT INTO  public.employee(fullname,email,password,position,photoprofile,payroll_number,token,company,plant) VALUES ('Dedi Sumarcell','audira98@gmail.com','seblak99',1,'http://jendelanasional.com/wp-content/uploads/2018/01/edi-setiawan.jpg','56983965','ogajJD5_Nd-AVqpxH7USxpTpV15cqkh9uF2127qd7y4.a78WR3uLYuWHSKKxU2kpry1k9cswGNGtGAd-FIByYa8','good company','good plant');

-- add data to material                             
INSERT INTO public.material(code,name) values ('MG-1002','Plant Rotating Machinery');
INSERT INTO public.material(code,name) values ('MG-1003','Plant Static Equipment');
INSERT INTO public.material(code,name) values ('MG-1004','Instrumentation Equipment and Part');
INSERT INTO public.material(code,name) values ('MG-1005','Electrical Equipment and Part');
INSERT INTO public.material(code,name) values ('MG-1006','Insulation Material');
INSERT INTO public.material(code,name) values ('MG-1007','Gasket and Packing Material');
INSERT INTO public.material(code,name) values ('MG-1008','Heavy Equipment and Part');
INSERT INTO public.material(code,name) values ('MG-1009','Transportation Equipment and Part');
INSERT INTO public.material(code,name) values ('MG-1010','Marine and Ship Equipment and Part');
INSERT INTO public.material(code,name) values ('MG-1011','Telecommunication, Electronic Equipment and Part');
INSERT INTO public.material(code,name) values ('MG-1012','Computer and Pheriperals');
INSERT INTO public.material(code,name) values ('MG-1013','Tools');

-- add data to request
INSERT INTO public.request(person_id,plant,budget_type,currency,expected_date, location, budget_source, justification, acc_scm, acc_manager, acc_owner,material,description,quatity,unit_measurement,record_id,process_id) values
(4,'thisIsPlant','thisIsBudget','thisIsCurrency','08/02/1996','Bandung','thisIsBudgetSource','thisIsJustification',0,0,0,25,'thisIsDescription',12,'thisIsUnitMeasurenment','thisIsRecordId','thisIsProcessId');
INSERT INTO public.request(person_id,plant,budget_type,currency,expected_date, location, budget_source, justification, acc_scm, acc_manager, acc_owner,material,description,quatity,unit_measurement,record_id,process_id) values
(4,'thisIsPlant','thisIsBudget','thisIsCurrency','08/02/1996','Bandung','thisIsBudgetSource','thisIsJustification',0,0,0,26,'thisIsDescription',12,'thisIsUnitMeasurenment','thisIsRecordId','thisIsProcessId');
INSERT INTO public.request(person_id,plant,budget_type,currency,expected_date, location, budget_source, justification, acc_scm, acc_manager, acc_owner,material,description,quatity,unit_measurement,record_id,process_id) values
(4,'thisIsPlant','thisIsBudget','thisIsCurrency','08/02/1996','Bandung','thisIsBudgetSource','thisIsJustification',0,0,0,27,'thisIsDescription',12,'thisIsUnitMeasurenment','thisIsRecordId','thisIsProcessId');

UPDATE employee set token = 'Dz0YjDWgEDZ6LOgF48i453y9gyh9lAKTJU-520GpmcA.LyxRqBfxUZskAu_rHa-NrtSvYwG3AMdqR4yo2wfeNz4' where id=4;