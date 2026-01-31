<template>
  <div class="container">
    <h1>HRMS Lite</h1>

    <!-- Add Employee -->
    <section class="card">
      <h2>Add Employee</h2>

      <div class="form-grid">
        <input v-model="employee.employee_id" placeholder="Employee ID" />
        <input v-model="employee.full_name" placeholder="Full Name" />
        <input v-model="employee.email" placeholder="Email" />
        <input v-model="employee.department" placeholder="Department" />
      </div>

      <button class="primary" @click="addEmployee">Add Employee</button>
      <p class="error" v-if="error">{{ error }}</p>
    </section>

    <!-- Employee List -->
    <section class="card">
      <h2>Employees</h2>

      <p v-if="employees.length === 0" class="muted">
        No employees added yet
      </p>

      <ul class="list">
        <li v-for="emp in employees" :key="emp.employee_id" class="list-item">
          <span>
            <strong>{{ emp.employee_id }}</strong> — {{ emp.full_name }}
          </span>

          <div class="actions">
            <button class="danger" @click="deleteEmployee(emp.employee_id)">
              Delete
            </button>
            <button class="secondary" @click="selectEmployee(emp.employee_id)">
              Attendance
            </button>
          </div>
        </li>
      </ul>
    </section>

    <!-- Attendance -->
    <section v-if="selectedEmployee" class="card">
      <h2>Attendance — {{ selectedEmployee }}</h2>

      <div class="form-row">
        <input type="date" v-model="attendance.date" />
        <select v-model="attendance.status">
          <option>Present</option>
          <option>Absent</option>
        </select>
        <button class="primary" @click="markAttendance">
          Mark Attendance
        </button>
      </div>

      <ul class="list">
        <li v-for="a in attendanceRecords" :key="a.date" class="list-item">
          {{ a.date }} — {{ a.status }}
        </li>
      </ul>
    </section>
  </div>
</template>

<script>
const API = "http://127.0.0.1:8000";

export default {
  data() {
    return {
      employee: {
        employee_id: "",
        full_name: "",
        email: "",
        department: ""
      },
      employees: [],
      attendance: {
        date: "",
        status: "Present"
      },
      attendanceRecords: [],
      selectedEmployee: null,
      error: ""
    };
  },

  mounted() {
    this.fetchEmployees();
  },

  methods: {
    async fetchEmployees() {
      const res = await fetch(`${API}/employees/`);
      this.employees = await res.json();
    },

    async addEmployee() {
      this.error = "";
      const res = await fetch(`${API}/employees/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(this.employee)
      });

      if (!res.ok) {
        const data = await res.json();
        this.error = data.detail;
        return;
      }

      this.employee = {
        employee_id: "",
        full_name: "",
        email: "",
        department: ""
      };

      this.fetchEmployees();
    },

    async deleteEmployee(id) {
      await fetch(`${API}/employees/${id}`, { method: "DELETE" });
      this.fetchEmployees();
    },

    async selectEmployee(id) {
      this.selectedEmployee = id;
      const res = await fetch(`${API}/attendance/${id}`);
      this.attendanceRecords = await res.json();
    },

    async markAttendance() {
      await fetch(`${API}/attendance/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          employee_id: this.selectedEmployee,
          date: this.attendance.date,
          status: this.attendance.status
        })
      });

      this.selectEmployee(this.selectedEmployee);
    }
  }
};
</script>

<style>
.container {
  max-width: 900px;
  margin: 40px auto;
  font-family: Arial, sans-serif;
}

h1 {
  text-align: center;
  margin-bottom: 30px;
}

.card {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  padding: 20px;
  margin-bottom: 24px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin-bottom: 12px;
}

.form-row {
  display: flex;
  gap: 10px;
  margin-bottom: 12px;
}

input,
select {
  padding: 8px;
  border: 1px solid #d1d5db;
  border-radius: 4px;
}

button {
  padding: 8px 14px;
  border-radius: 4px;
  border: none;
  cursor: pointer;
}

.primary {
  background: #2563eb;
  color: white;
}

.secondary {
  background: #e5e7eb;
}

.danger {
  background: #dc2626;
  color: white;
}

.list {
  list-style: none;
  padding: 0;
}

.list-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #e5e7eb;
}

.actions {
  display: flex;
  gap: 8px;
}

.error {
  color: #dc2626;
  margin-top: 8px;
}

.muted {
  color: #6b7280;
}
</style>
