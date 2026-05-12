class Department:
    def __init__(self, deptID, name):
        self.deptID = deptID
        self.name = name

    @property
    def deptID(self):
        return self._deptID
    
    @deptID.setter
    def deptID(self, val):
        if not isinstance(val, int):
            raise ValueError("ID must be an integer")
        if val < 0:
            raise ValueError("DeptID cannot be negative")
        self._deptID = val

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, val):
        if not isinstance(val, str):
            raise ValueError("Name must be a string")

        self._name = val 

class Employee:
    def __init__(self, id, name, salary, dept):
        self.id = id
        self.name = name
        self.salary = salary
        self.dept = dept

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, val):
        if not isinstance(val, int):
            raise ValueError("ID must be an integer")
        if val < 0:
            raise ValueError("ID cannot be negative")
        self._id = val

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        if not isinstance(val, str):
            raise ValueError("Name must be a string")
        self._name = val

    @property
    def salary(self):
        return self._salary

    @salary.setter
    def salary(self, val):
        if not isinstance(val, (int, float)):
            raise ValueError("Salary must be a number")
        if val < 0:
            raise ValueError("Salary cannot be negative")
        self._salary = val

    @property
    def dept(self):
        return self._dept

    @dept.setter
    def dept(self, val):
        if not isinstance(val, Department):
            raise ValueError("dept must be a Department instance")
        self._dept = val

    @staticmethod
    def print_employees(employees):
        print('All Employees: ID, Name, Salary, Department (Dept ID)')
        for employee in employees:
            print(f'{employee.id}, {employee.name}, {employee.salary}, {employee.dept.name} ({employee.dept.deptID})')

    @staticmethod
    def delete_employee(employees, employee_id):
        target_employee = None
        for employee in employees:
            if employee.id == employee_id:
                target_employee = employee
                break
        
        employees.remove(target_employee)
        print(f"Employee {employee_id} deleted successfully")

    
    @staticmethod
    def modify_employee(employees, employee_id, attribute, new_val):
        target_emp = None
        for emp in employees:
            if emp.id == employee_id:
                target_emp = emp
                break
        
        if not target_emp:
            print(f"Employee with ID {employee_id} not found")
            return

        if attribute == 'id':
            target_emp.id = new_val
        elif attribute == 'name':
            target_emp.name = new_val
        elif attribute == 'salary':
            target_emp.salary = new_val
        elif attribute == 'dept':
            target_emp.dept = new_val
        else:
            print(f'Invalid attribute: {attribute}')
            return
        
        print(f"Employee {employee_id}'s {attribute} updated successfully")

# Departments
engineering = Department(1, "Engineering")
marketing = Department(2, "Marketing")
finance = Department(3, "Finance")

# Employees
emp1 = Employee(101, "Alice Johnson", 85000, engineering)
emp2 = Employee(102, "Bob Smith", 72000, engineering)
emp3 = Employee(103, "Carol White", 91000, marketing)
emp4 = Employee(104, "David Brown", 67000, finance)
emp5 = Employee(105, "Eva Martinez", 78000, marketing)

employees = [emp1, emp2, emp3, emp4, emp5]

Employee.print_employees(employees)

print()
Employee.delete_employee(employees, 103)
print()


Employee.print_employees(employees)

#employees[2].dept = marketing
#print('\nDavid switched to marketing department\n')
print('\n')
Employee.modify_employee(employees, 104, 'dept', marketing)
print('\n')


Employee.print_employees(employees)
