import { useMsal } from "@azure/msal-react";

function handleLogout(instance) {
    instance.logoutPopup().catch(e => {
        console.error(e);
    });
}

/**
 * Renders a button which, when selected, will open a popup for logout
 */
export const SignOutButton = () => {
    const { instance } = useMsal();

    return (
        <button className="button is-light" onClick={() => handleLogout(instance)}>Sign out</button>
    );
}