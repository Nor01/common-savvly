import React, { useContext, useState } from "react";

const AppContext = React.createContext();

export function useAppContext() {
    return useContext(AppContext);
}

export const AppContextProvider = ({children}) => {
    const [showSideBar, setShowSideBar] = useState(true);

    return (
        <AppContext.Provider
            value={{
                showSideBar,
                setShowSideBar
            }}>
            {children}
        </AppContext.Provider>
    );
}