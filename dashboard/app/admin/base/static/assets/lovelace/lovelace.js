function saveSettings(key, value) {
  localStorage.setItem(key, value);
}

function getSettings(key) {
  return localStorage.getItem(key);
}

function removeSettings(key) {
  localStorage.removeItem(key);
}