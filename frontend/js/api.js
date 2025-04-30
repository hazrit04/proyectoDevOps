const API_URL = "https://tu-backend.azurewebsites.net"; // cambia esta URL si es local

function getToken() {
  return localStorage.getItem("token");
}

function setToken(token) {
  localStorage.setItem("token", token);
}

function removeToken() {
  localStorage.removeItem("token");
}
