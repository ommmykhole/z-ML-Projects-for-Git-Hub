CREATE DATABASE company_db;

USE company_db;

CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    employee_name VARCHAR(50),
    department VARCHAR(30),
    salary INT,
    age INT,
    city VARCHAR(30)
);

INSERT INTO employees
(employee_id, employee_name, department, salary, age, city)
VALUES
(1, 'Amit', 'IT', 55000, 25, 'Pune'),
(2, 'Rahul', 'HR', 72000, 29, 'Mumbai'),
(3, 'Neha', 'IT', 85000, 31, 'Pune'),
(4, 'Priya', 'Sales', 48000, 24, 'Nashik'),
(5, 'Karan', 'HR', 65000, 28, 'Mumbai'),
(6, 'Sneha', 'Finance', 92000, 34, 'Pune'),
(7, 'Rohit', 'Sales', 52000, 26, 'Nashik'),
(8, 'Pooja', 'IT', 75000, 27, 'Pune'),
(9, 'Akash', 'Finance', 88000, 30, 'Mumbai'),
(10, 'Riya', 'HR', 58000, 23, 'Mumbai'),
(11, 'Varun', 'Marketing', 45000, 22, 'Pune'),
(12, 'Anjali', 'Marketing', 47000, 25, 'Pune'),
(13, 'Vikas', 'IT', 68000, 26, 'Pune'),
(14, 'Meera', 'Sales', 61000, 29, 'Nashik'),
(15, 'Sahil', 'Finance', 78000, 27, 'Pune');




select * from employees;






select * from employees 
where salary > (select avg(salary) from employees);





select * from employees 
where salary < (select avg(salary) from employees);






select * from employees 
where salary = (select max(salary) from employees);





select * from employees 
where salary = (select min(salary) from employees);







select * from employees 
where age > (select avg(age) from employees);









select * from employees 
where salary > (select avg(salary)
from employees 
where department = "IT");








select * from employees 
where salary = (select avg(salary)
from employees 
where department = "HR");





select * from employees 
where salary > (select max(salary) from employees 
where department = "sales");








select * from employees 
where salary < (select min(salary) from employees 
where department = "Finance");








select * from employees 
where age > (select avg(age) from employees 
where department = "IT");








select * from employees 
where salary > any(select salary from employees 
where department = "HR");







select * from employees 
where salary > all(select salary from employees 
where department = "HR");









select * from employees 
where salary < any (select salary from employees 
where department = "Sales");







select * from employees 
where salary < all(select salary from employees 
where department = "sales");







select d.department, d.avg_salary from (
select department,avg(salary)as avg_salary from employees 
group by department)as d;







select department, avg(salary)as Average_salary 
from employees 
group by department
having avg(salary) > (select avg(salary)
from employees);











select employee_name, salary, (select avg(salary)
from employees)as Company_Avg_Salary
from employees;








select * from employees 
where salary > (select avg(salary) from employees);










select e.employee_name, e.department
from employees e 
where e.salary > (select max(e2.salary)
from employees e2 
where e2.department = e.department );









select e.employee_name, e.department_id, e.salary
from employees e
where e.salary > (
    select avg(e2.salary)
    from employees e2
    where e2.department = e.department
)
and e.salary > (
    select avg(salary)
    from employees
);






























