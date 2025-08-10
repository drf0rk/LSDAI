// Custom JavaScript for LSDAI Widgets

/**
 * Toggles the 'expanded' class on the collapsible container.
 * This function is designed to be called by an 'onclick' event from an HTML widget.
 * The accompanying CSS in main.css handles the actual height transition animation.
 */
function toggleContainer() {
    const container = document.querySelector('.collapsible-container');
    if (container) {
        container.classList.toggle('expanded');
    }
}
