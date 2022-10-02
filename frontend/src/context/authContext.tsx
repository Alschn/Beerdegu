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

interface AuthProviderProps {
  children: ReactNode;
}

export interface JWTContent {
  user_id: number,
  first_name: string,
  last_name: string,
  email: string,
  position: string
}

interface AuthContextProps {
  token: JWTContent | null,
  refreshToken: string | null,
  setToken: Dispatch<SetStateAction<JWTContent | null>>,
  setRefreshToken: Dispatch<SetStateAction<string | null>>,
  logout: () => void,
  isAuthenticated: boolean
}

const AuthContext = createContext<AuthContextProps>({} as AuthContextProps);

export const useAuth = () => useContext(AuthContext);

const AuthProvider: FC<AuthProviderProps> = ({children}) => {
  const [token, setToken] = useState<JWTContent | null>(() => {
    const jwt_token = localStorage.getItem('token');
    if (!jwt_token) return null;
    return jwtDecode<JWTContent>(jwt_token);
  });

  // it would be nice if axios interceptor could use this
  // might remove this later
  const [refreshToken, setRefreshToken] = useState<string | null>(null);

  const logout = useCallback(() => {
    // remove token either way;
    // even though user might still be logged on the backend with old creds

    return onLogout().finally(() => {
      localStorage.removeItem('token');
      setToken(null);
    });
  }, []);

  const isAuthenticated = useMemo(() => {
    return token !== null;
  }, [token]);

  return (
    <AuthContext.Provider value={{token, refreshToken, setRefreshToken, setToken, logout, isAuthenticated}}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;
