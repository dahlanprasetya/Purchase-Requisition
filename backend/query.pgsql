DROP DATABASE pr_makers;
CREATE DATABASE pr_makers;
-- DELETE from request;
-- SELECT * from kelas;
-- Drop table request;

-- View data
select * from public.position;
select * from public.employee;
select * from public.material;
select * from request;
select * from items;

-- add data to position
insert into position(name) values ('Owner');
insert into position(name) values ('Manager');
insert into position(name) values ('SCM');
insert into position(name) values ('Employee');

-- add data to employee

INSERT INTO  public.employee(fullname,email,password,position,photoprofile,payroll_number,token,company,plant) VALUES ('Jhon Pantau','ahaydeuh69@gmail.com','c2VibGFrOTk=',4,'https://cdn.idntimes.com/content-images/post/20170816/20399049-1947030192252857-366213070848000000-n-e5b1de42acf427b1a73b795f839388fe_600x400.jpg','72983927','QJW6h1tISjYqGmxM91s_kIKeUvDzu26asyzem2Unqm8.EMHXC5ZHMEOZnrGNmew6aBxqGNZH0DS3cqB87Fr0a_M','good company','good plant');
INSERT INTO  public.employee(fullname,email,password,position,photoprofile,payroll_number,token,company,plant) VALUES ('Robert Tantular','oka.aryanata9@gmail.com','c2VibGFrOTk=',3,'https://banner2.kisspng.com/20180824/hfj/kisspng-portable-network-graphics-businessperson-jpeg-wind-resume-writing-services-canberra-rev-up-your-resu-5b7fd44917e9f0.179883131535104073098.jpg','72983939','cucFlgpukUJ5Wl2UGLq22yGBDyeZWYgdPhhb8mcZKSw.pEveDPIlnvdGq_uLRypv1ufu-93XqnTFrVAawd0UM_Q','good company','good plant');
INSERT INTO  public.employee(fullname,email,password,position,photoprofile,payroll_number,token,company,plant) VALUES ('Asep Junaidi','okaaryanata@gmail.com','c2VibGFrOTk=',2,'https://i1.wp.com/www.jabarsatu.com/wp-content/uploads/2014/12/gayus.jpg?fit=311%2C310&ssl=1','43983934','300lxXNPTsRBbolPlCnv3JQPyrT0M5WhS202HhHcpjE.xhdkL7R_83rBq7UQTDfxyepP8tSumgJgZdUvPtqOzO8','good company','good plant');
INSERT INTO  public.employee(fullname,email,password,position,photoprofile,payroll_number,token,company,plant) VALUES ('Dedi Sumarcell','audira98@gmail.com','c2VibGFrOTk=',1,'http://jendelanasional.com/wp-content/uploads/2018/01/edi-setiawan.jpg','56983965','bVba2uuQAqwPe77-kvyNwUPb6Ab8-NWvmzPCFFIbH-Q.CWBzB0eEOdnWeZZOVOtbPNyi33TLVPBKGyE0VWKLIQM','good company','good plant');
INSERT INTO  public.employee(fullname,email,password,position,photoprofile,payroll_number,token,company,plant) VALUES ('Kumis Kucing','kumiskucinglegit@gmail.com','c2VibGFrOTk=',4,'https://cdn.idntimes.com/content-images/post/20170816/20399049-1947030192252857-366213070848000000-n-e5b1de42acf427b1a73b795f839388fe_600x400.jpg','72983927','QJW6h1tISjYqGmxM91s_kIKeUvDzu26asyzem2Unqm8.EMHXC5ZHMEOZnrGNmew6aBxqGNZH0DS3cqB87Fr0a_M','good company','good plant');

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
-- INSERT INTO public.request(person_id,plant,budget_type,currency,expected_date, location, budget_source, justification, acc_scm, acc_manager, acc_owner,material,description,quatity,unit_measurement,record_id,process_id) values
-- (4,'thisIsPlant','thisIsBudget','thisIsCurrency','08/02/1996','Bandung','thisIsBudgetSource','thisIsJustification',0,0,0,25,'thisIsDescription',12,'thisIsUnitMeasurenment','thisIsRecordId','thisIsProcessId');
-- INSERT INTO public.request(person_id,plant,budget_type,currency,expected_date, location, budget_source, justification, acc_scm, acc_manager, acc_owner,material,description,quatity,unit_measurement,record_id,process_id) values
-- (4,'thisIsPlant','thisIsBudget','thisIsCurrency','08/02/1996','Bandung','thisIsBudgetSource','thisIsJustification',0,0,0,26,'thisIsDescription',12,'thisIsUnitMeasurenment','thisIsRecordId','thisIsProcessId');
-- INSERT INTO public.request(person_id,plant,budget_type,currency,expected_date, location, budget_source, justification, acc_scm, acc_manager, acc_owner,material,description,quatity,unit_measurement,record_id,process_id) values
-- (4,'thisIsPlant','thisIsBudget','thisIsCurrency','08/02/1996','Bandung','thisIsBudgetSource','thisIsJustification',0,0,0,27,'thisIsDescription',12,'thisIsUnitMeasurenment','thisIsRecordId','thisIsProcessId');

UPDATE employee set token = 'RmPvmg1lNpBqXzJW1cSKuCEhuvS9pe3__Kebc-lZpcM.PC9hsLq4vwvvyGOongpCyJIioh-bK7ycogjp3HwHEhY' where id=4;
UPDATE employee set token = '7SRxLYTCWbkoNRxbAqCcwFF2xcP-f9xE2niSP2u8DZ0.HTzvB_BcEbXjYa6kTFvhCMtEveqVlQ6L_PK551ae5O0' where id=3;
UPDATE employee set token = 'RIaC4iaC1euFq84KRBOjTBuDK-dCjqYw8GaJ7lIiz-I.87uvFkDfUwWczfk2XxWEl80vykGozpRYnAAhdeYrSHI' where id=2;
UPDATE employee set token = 'ev3pjPWAum4CeswvIkw9pO-6KqVIfMyulG6Fu_o36WA.hHrLmRjWiUv3EcHHY9CoWLY2dgVOdobnhye_abm5--4' where id=1;
UPDATE employee set token = 'ev3pjPWAum4CeswvIkw9pO-6KqVIfMyulG6Fu_o36WA.hHrLmRjWiUv3EcHHY9CoWLY2dgVOdobnhye_abm5--4' where id=5;

-- UPDATE employee set password = 'c2VibGFrOTk=' where id=4;
-- UPDATE employee set password = 'c2VibGFrOTk=' where id=3;
-- UPDATE employee set password = 'c2VibGFrOTk=' where id=2;
-- UPDATE employee set password = 'c2VibGFrOTk=' where id=1;