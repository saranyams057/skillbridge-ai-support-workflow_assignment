import axios from "axios";

const API_BASE_URL = "http://localhost:8000";

export async function sendMessage(message, state) {
  const response = await axios.post(`${API_BASE_URL}/api/chat`, {
    message,
    state,
  });
  return response.data;
}

export async function getInitialState() {
  const response = await axios.get(`${API_BASE_URL}/api/state`);
  return response.data;
}
