export const WS_SCHEME = window.location.protocol === 'https' ? 'wss': 'ws';
export const HOST = window.location.hostname === '127.0.0.1' ? '127.0.0.1:8000' : window.location.host;
