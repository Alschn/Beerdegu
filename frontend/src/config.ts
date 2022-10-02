let BACKEND_URL = process.env.REACT_APP_BACKEND_URL as string;
let WEBSOCKET_URL = process.env.REACT_APP_WEBSOCKET_URL as string;

if (process.env.NODE_ENV === 'production') {
  // had to use this hack because of heroku cannot use config vars build time for some stupid reason
  BACKEND_URL = 'https://beerdegu.herokuapp.com';
  WEBSOCKET_URL = 'wss://beerdegu.herokuapp.com';
}

if (!BACKEND_URL) {
  throw new Error('Missing `REACT_APP_BACKEND_URL` environment variable. Example `http://127.0.0.1:8000`');
}

if (!WEBSOCKET_URL) {
  throw new Error('Missing `REACT_APP_WEBSOCKET_URL` environment variable. Example: `ws://127.0.0.1:8000`');
}

export {WEBSOCKET_URL, BACKEND_URL};
