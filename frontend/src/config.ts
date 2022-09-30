const BACKEND_URL = process.env.REACT_APP_BACKEND_URL as string;
const WEBSOCKET_URL = process.env.REACT_APP_WEBSOCKET_URL as string;


if (!BACKEND_URL) {
  throw new Error('Missing `REACT_APP_BACKEND_URL` environment variable. Example `http://127.0.0.1:8000`');
}

if (!WEBSOCKET_URL) {
  throw new Error('Missing `REACT_APP_WEBSOCKET_URL` environment variable. Example: `ws://127.0.0.1:8000`');
}

export {WEBSOCKET_URL, BACKEND_URL};
