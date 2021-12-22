import {createContext} from "react";

interface AuthContextProps {

}

export const AuthContext = createContext<AuthContextProps>({});

const AuthContextProvider = () => {
  return (
    <AuthContext.Provider value={{}}>

    </AuthContext.Provider>
  );
};

export default AuthContextProvider;
