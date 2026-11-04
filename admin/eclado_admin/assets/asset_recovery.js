// Recover stale/lost Streamlit widget chunks without bypassing the login gate.
export default function(component) {
    if (window.__ecladoAssetRecoveryInstalled) return;
    window.__ecladoAssetRecoveryInstalled = true;
    const key = `eclado.asset-recovery.${component.data.revision}`;
    window.addEventListener("vite:preloadError", event => {
        const message = String(event.payload?.message || event.payload || "");
        if (!/Failed to fetch dynamically imported module|Importing a module script failed|Unable to preload CSS|error loading dynamically imported module/i.test(message)) return;
        try {
            // A second failure stays visible. Never keep reloading a broken deployment.
            if (sessionStorage.getItem(key)) return;
            sessionStorage.setItem(key, "reloaded");
        } catch {
            return; // Cannot enforce the reload limit when storage is blocked.
        }
        event.preventDefault();
        window.location.reload();
    });
}
