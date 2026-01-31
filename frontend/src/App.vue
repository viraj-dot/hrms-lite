<template>
  <div style="max-width: 800px; margin: auto; font-family: Arial;">
    <h1>HRMS Lite</h1>

    <!-- Add Employee -->
    <section>
      <h2>Add Employee</h2>
      <input v-model="employee.employee_id" placeholder="Employee ID" />
      <input v-model="employee.full_name" placeholder="Full Name" />
      <input v-model="employee.email" placeholder="Email" />
      <input v-model="employee.department" placeholder="Department" />
      <button @click="addEmployee">Add</button>
      <p style="color:red">{{ error }}</p>
    </section>

    <hr />

    <!-- Employee List -->
    <section>
      <h2>Employees</h2>
      <ul>
        <li v-for="emp in employees" :key="emp.employee_id">
          {{ emp.employee_id }} - {{ emp.full_name }}
          <button @click="deleteEmployee(emp.employee_id)">Delete</button>
          <button @click="selectEmployee(emp.employee_id)">Attendance</button>
        </li>
      </ul>
    </section>

    <hr />

    <!-- Attendance -->
    <section v-if="selectedEmployee">
      <h2>Attendance for {{ selectedEmployee }}</h2>

      <input type="date" v-model="attendance.date" />
      <select v-model="attendance.status">
        <option>Present</option>
        <option>Absent</option>
      </select>
      <button @click="markAttendance">Mark</button>

      <ul>
        <li v-for="a in attendanceRecords" :key="a.date">
          {{ a.date }} - {{ a.status }}
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
      const res = await fetch(`${API}/employees`);
      this.employees = await res.json();
    },

    async addEmployee() {
      this.error = "";
      const res = await fetch(`${API}/employees`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(this.employee)
      });

      if (!res.ok) {
        const data = await res.json();
        this.error = data.detail;
        return;
      }

      this.employee = { employee_id: "", full_name: "", email: "", department: "" };
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
      await fetch(`${API}/attendance`, {
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
/* basic styles can go here */
</style>
