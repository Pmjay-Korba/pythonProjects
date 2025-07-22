from playwright.sync_api import sync_playwright, Page, TimeoutError

def inject_department(page: Page, button_names: list):
    return page.evaluate("""
        (buttonNames) => {
            return new Promise((resolve) => {
                function createCustomConfirm(message, callback) {
                    const modalBackground = document.createElement('div');
                    modalBackground.style.position = 'fixed';
                    modalBackground.style.top = '0';
                    modalBackground.style.left = '0';
                    modalBackground.style.width = '100%';
                    modalBackground.style.height = '100%';
                    modalBackground.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
                    modalBackground.style.display = 'flex';
                    modalBackground.style.alignItems = 'center';
                    modalBackground.style.justifyContent = 'center';
                    modalBackground.style.zIndex = '10000';

                    const modalContent = document.createElement('div');
                    modalContent.style.backgroundColor = 'white';
                    modalContent.style.padding = '20px';
                    modalContent.style.borderRadius = '10px';
                    modalContent.style.boxShadow = '0 0 10px rgba(0, 0, 0, 0.1)';
                    modalContent.style.textAlign = 'center';
                    modalContent.style.maxWidth = '300px';

                    // FIX: Use textContent instead of innerHTML to avoid TrustedHTML issues
                    modalContent.textContent = message;

                    const buttonsContainer = document.createElement('div');
                    buttonsContainer.style.marginTop = '20px';

                    const yesButton = document.createElement('button');
                    yesButton.innerHTML = 'Yes';
                    yesButton.style.margin = '0 10px';
                    yesButton.style.padding = '10px 20px';
                    yesButton.style.backgroundColor = '#266ab5';
                    yesButton.style.color = 'white';
                    yesButton.style.border = 'none';
                    yesButton.style.borderRadius = '8px';
                    yesButton.style.cursor = 'pointer';
                    yesButton.style.width = '100px';
                    yesButton.onclick = () => {
                        modalBackground.remove();
                        callback(true);
                    };

                    const cancelButton = document.createElement('button');
                    cancelButton.innerHTML = 'Cancel';
                    cancelButton.style.margin = '0 10px';
                    cancelButton.style.padding = '10px 20px';
                    cancelButton.style.backgroundColor = '#266ab5';
                    cancelButton.style.color = 'white';
                    cancelButton.style.border = 'none';
                    cancelButton.style.borderRadius = '8px';
                    cancelButton.style.cursor = 'pointer';
                    cancelButton.style.width = '100px';
                    cancelButton.onclick = () => {
                        modalBackground.remove();
                        callback(false);
                    };

                    buttonsContainer.appendChild(yesButton);
                    buttonsContainer.appendChild(cancelButton);
                    modalContent.appendChild(buttonsContainer);
                    modalBackground.appendChild(modalContent);
                    document.body.appendChild(modalBackground);
                }

                const existingContainer = document.getElementById('customButtonContainer');
                if (existingContainer) {
                    existingContainer.remove();
                }

                const container = document.createElement('div');
                container.id = 'customButtonContainer';
                let selectedButtonName = '';

                buttonNames.forEach(name => {
                    const button = document.createElement('button');
                    button.innerHTML = name;
                    button.style.margin = '20px auto';
                    button.style.display = 'block';
                    button.style.width = '100%';
                    button.style.padding = '10px';
                    button.style.backgroundColor = '#15db06';
                    button.style.color = 'white';
                    button.style.border = 'none';
                    button.style.borderRadius = '8px';
                    button.style.cursor = 'pointer';
                    button.style.fontSize = '10px';

                    button.onclick = () => {
                        selectedButtonName = name;
                        const message = `You clicked on ${name}`;
                        createCustomConfirm(message, confirmClick => {
                            if (confirmClick) {
                                container.remove();
                                resolve(selectedButtonName);
                            }
                        });
                    };

                    container.appendChild(button);
                });

                document.body.appendChild(container);
                container.style.position = 'fixed';
                container.style.bottom = '10px';
                container.style.right = '10px';
                container.style.width = '150px';
                container.style.zIndex = '10000';
                container.style.backgroundColor = 'rgb(221,221,221)';
                container.style.padding = '5px';
                container.style.borderRadius = '8px';
                container.style.boxShadow = '0px 0px 10px rgba(0, 0, 0, 0.1)';
            });
        }
    """, button_names)

