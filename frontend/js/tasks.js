// Validación de token y redirección si no hay sesión
if (!getToken()) {
    window.location.href = "login.html";
  }
  
  const form = document.getElementById("task-form");
  const tbody = document.getElementById("tasks-body");
  
  // Cargar tareas al iniciar
  document.addEventListener("DOMContentLoaded", loadTasks);
  
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
  
    const title = document.getElementById("title").value;
    const description = document.getElementById("description").value;
  
    const response = await fetch(`${API_URL}/tasks`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${getToken()}`
      },
      body: JSON.stringify({ title, description })
    });
  
    if (response.ok) {
      form.reset();
      loadTasks();
    } else {
      alert("Error al crear tarea");
    }
  });
  
  async function loadTasks() {
    const response = await fetch(`${API_URL}/tasks`, {
      headers: {
        Authorization: `Bearer ${getToken()}`
      }
    });
  
    if (!response.ok) {
      alert("No se pudieron cargar las tareas");
      return;
    }
  
    const tasks = await response.json();
    tbody.innerHTML = "";
  
    tasks.forEach(task => {
      const row = document.createElement("tr");
  
      row.innerHTML = `
        <td>${task.title}</td>
        <td>${task.description}</td>
        <td>${task.state}</td>
        <td>
          <button class="btn btn-sm btn-primary me-2" onclick="editTask(${task.task_id})">Editar</button>
          <button class="btn btn-sm btn-danger" onclick="deleteTask(${task.task_id})">Eliminar</button>
        </td>
      `;
  
      tbody.appendChild(row);
    });
  }
  
  async function deleteTask(id) {
    if (!confirm("¿Eliminar esta tarea?")) return;
  
    const response = await fetch(`${API_URL}/tasks/${id}`, {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${getToken()}`
      }
    });
  
    if (response.ok) {
      loadTasks();
    } else {
      alert("Error al eliminar tarea");
    }
  }
  
  async function editTask(id) {
    const title = prompt("Nuevo título:");
    const description = prompt("Nueva descripción:");
  
    if (!title || !description) return;
  
    const response = await fetch(`${API_URL}/tasks/${id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${getToken()}`
      },
      body: JSON.stringify({ title, description, state: "pendiente" }) // puedes cambiar el estado
    });
  
    if (response.ok) {
      loadTasks();
    } else {
      alert("Error al actualizar tarea");
    }
  }
  
  function logout() {
    removeToken();
    window.location.href = "login.html";
  }
  