import {
  createContext,
  Dispatch,
  FC,
  ReactNode,
  SetStateAction,
  useCallback,
  useContext,
  useMemo,
  useState
} from "react";
import jwtDecode from "jwt-decode";
import {onLogout} from "../api/auth";
import {ACCESS_TOKEN_KEY, REFRESH_TOKEN_KEY} from "../config";

interface AuthProviderProps {
  children: ReactNode;
}

export interface JWTContent {
  user_id: number,
  username: string,
}

interface AuthContextProps {
  token: JWTContent | null,
  setToken: Dispatch<SetStateAction<JWTContent | null>>,
  logout: () => void,
  isAuthenticated: boolean
}

const AuthContext = createContext<AuthContextProps>({} as AuthContextProps);

export const useAuth = () => useContext(AuthContext);

const AuthProvider: FC<AuthProviderProps> = ({children}) => {
  const [token, setToken] = useState<JWTContent | null>(() => {
    const jwt_token = localStorage.getItem(ACCESS_TOKEN_KEY);
    if (!jwt_token) return null;
    return jwtDecode<JWTContent>(jwt_token);
  });

  const logout = useCallback(() => {
    // remove token either way;
    // even though user might still be logged on the backend with old creds

    return onLogout().finally(() => {
      localStorage.removeItem(ACCESS_TOKEN_KEY);
      localStorage.removeItem(REFRESH_TOKEN_KEY);
      setToken(null);
    });
  }, []);

  const isAuthenticated = useMemo(() => {
    return token !== null;
  }, [token]);

  return (
    <AuthContext.Provider value={{token, setToken, logout, isAuthenticated}}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;
