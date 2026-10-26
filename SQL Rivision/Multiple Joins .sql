select * from cities;
select * from departments;
select * from employees;








select e.employee_name, d.department_name, e.salary
from employees e 
inner join departments d 
on d.department_id = e.department_id;








select e.employee_name, d.department_name 
from employees e 
join departments d 
on d.department_id = e.department_id;







select d.department_name, e.employee_name
from employees e 
right join departments d 
on e.department_id = d.department_id;







select e.employee_name, d.department_name,d.department_id
from departments d 
join employees e 
on d.department_id = e.department_id 
where e.employee_name is null;









select d.department_name, e.employee_name
from departments d 
join employees e 
on d.department_id = e.department_id
where d.department_id is null;









select e.employee_name as employee,
m.employee_name as manager
from employees e 
join employees m 
on e.emp_id = m.manager_id;









select e.employee_name, e.salary , d.department_name, c.city_name
from employees e 
join departments d 
on d.department_id = e.department_id 
join cities c 
on c.city_id = e.city_id
where d.department_name = "IT" and c.city_name = "Pune";








select e.employee_name as employee,
m.employee_name as manager,
d.department_name,
e.salary
from employees e 
join employees m 
on e.emp_id = m.manager_id
join departments d 
on d.department_id = e.department_id 
order by e.salary desc;








select e.employee_name as Employee,
m.employee_name as Manager,
d.department_name, c.city_name, e.salary
from employees e 
join employees m 
on m.emp_id = e.manager_id
join departments d 
on d.department_id = e.department_id
join cities c 
on e.city_id = c.city_id
where e.salary > 55000 and d.department_name in ("IT","HR") and c.city_name in ("Pune","Mumbai")
order by e.salary desc;




















