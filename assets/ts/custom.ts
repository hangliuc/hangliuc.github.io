const storageKey = 'right-sidebar-collapsed';
const collapsedClass = 'right-sidebar-collapsed';
const initializedAttribute = 'sidebarToggleInitialized';

const initRightSidebarToggle = () => {
    const mainContainer = document.querySelector('.main-container') as HTMLElement | null;
    const toggle = document.getElementById('toggle-right-sidebar') as HTMLButtonElement | null;
    const rightSidebar = document.getElementById('right-sidebar') as HTMLElement | null;

    if (!mainContainer || !toggle || !rightSidebar) return false;

    const positionToggle = (collapsed: boolean) => {
        if (collapsed) {
            toggle.style.left = '';
            toggle.style.right = '12px';
            return;
        }

        const sidebarLeft = rightSidebar.getBoundingClientRect().left;
        toggle.style.left = `${Math.max(8, sidebarLeft - toggle.offsetWidth)}px`;
        toggle.style.right = 'auto';
    };

    const setCollapsed = (collapsed: boolean) => {
        mainContainer.classList.toggle('right-sidebar-collapsed', collapsed);
        toggle.setAttribute('aria-expanded', String(!collapsed));

        const label = collapsed
            ? toggle.dataset.expandLabel
            : toggle.dataset.collapseLabel;

        if (label) {
            toggle.setAttribute('aria-label', label);
            toggle.setAttribute('title', label);
            toggle.setAttribute('data-current-label', label);
        }

        const icon = toggle.querySelector('.right-sidebar-toggle__icon');
        if (icon) {
            icon.textContent = collapsed ? '›' : '‹';
        }

        const text = toggle.querySelector('.right-sidebar-toggle__text');
        if (text && label) text.textContent = label;

        window.requestAnimationFrame(() => positionToggle(collapsed));
    };

    const getSavedState = () => {
        try {
            return window.localStorage.getItem(storageKey) === 'true';
        } catch {
            return false;
        }
    };

    const saveState = (collapsed: boolean) => {
        try {
            window.localStorage.setItem(storageKey, String(collapsed));
        } catch {
            // The toggle still works when persistent storage is unavailable.
        }
    };

    // A page restored from the browser cache may keep the button DOM but lose
    // its event binding. Reposition it without binding a second listener.
    if (toggle.dataset[initializedAttribute] === 'true') {
        window.requestAnimationFrame(() => positionToggle(mainContainer.classList.contains(collapsedClass)));
        return true;
    }

    setCollapsed(getSavedState());

    toggle.addEventListener('click', () => {
        const collapsed = !mainContainer.classList.contains(collapsedClass);
        setCollapsed(collapsed);
        saveState(collapsed);
    });

    toggle.dataset[initializedAttribute] = 'true';

    window.addEventListener('resize', () => {
        positionToggle(mainContainer.classList.contains(collapsedClass));
    });

    return true;
};

const bootRightSidebarToggle = () => {
    // Run on the next frame so the sidebar has finished its first layout.
    window.requestAnimationFrame(() => {
        initRightSidebarToggle();
    });
};

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', bootRightSidebarToggle, { once: true });
} else {
    bootRightSidebarToggle();
}

// `pageshow` covers bfcache restores and browser refreshes that reuse the
// existing document. `load` is a second safe point for slow layout/assets.
window.addEventListener('pageshow', bootRightSidebarToggle);
window.addEventListener('load', bootRightSidebarToggle, { once: true });
