let BACKEND_URL = import.meta.env.VITE_BACKEND_URL as string;
let WEBSOCKET_URL = import.meta.env.VITE_WEBSOCKET_URL as string;

if (import.meta.env.PROD) {
  // had to use this hack because of heroku cannot use config vars build time for some stupid reason
  BACKEND_URL = 'https://beerdegu.herokuapp.com';
  WEBSOCKET_URL = 'wss://beerdegu.herokuapp.com';
}

if (!BACKEND_URL) {
  throw new Error('Missing `VITE_BACKEND_URL` environment variable. Example `http://127.0.0.1:8000`');
}

if (!WEBSOCKET_URL) {
  throw new Error('Missing `VITE_WEBSOCKET_URL` environment variable. Example: `ws://127.0.0.1:8000`');
}

const ACCESS_TOKEN_KEY = 'token';
const REFRESH_TOKEN_KEY = 'refresh';

export {
  WEBSOCKET_URL,
  BACKEND_URL,
  ACCESS_TOKEN_KEY,
  REFRESH_TOKEN_KEY,
};
