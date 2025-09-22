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

async def modal_info_button(page, message: str):
    await page.evaluate(
        """(customMessage) => {
            return new Promise((resolve) => {
                // Modal overlay (blocks background)
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

                // Modal box
                const modalContent = document.createElement('div');
                modalContent.style.backgroundColor = 'white';
                modalContent.style.padding = '20px';
                modalContent.style.borderRadius = '10px';
                modalContent.style.boxShadow = '0 0 10px rgba(0, 0, 0, 0.1)';
                modalContent.style.textAlign = 'center';
                modalContent.style.maxWidth = '400px';

                // Add message
                const messageDiv = document.createElement('div');
                messageDiv.innerHTML = customMessage;
                messageDiv.style.marginBottom = '20px';
                modalContent.appendChild(messageDiv);

                // Add CONTINUE button
                const continueButton = document.createElement('button');
                continueButton.innerHTML = '<b>CONTINUE</b>';
                continueButton.style.padding = '10px 20px';
                continueButton.style.backgroundColor = '#266ab5';
                continueButton.style.color = 'white';
                continueButton.style.border = 'none';
                continueButton.style.borderRadius = '8px';
                continueButton.style.cursor = 'pointer';
                continueButton.style.width = '120px';
                continueButton.onclick = () => {
                    modalBackground.remove();
                    resolve("CONTINUE");
                };

                modalContent.appendChild(continueButton);
                modalBackground.appendChild(modalContent);
                document.body.appendChild(modalBackground);
            });
        }""",
        message
    )

import os, subprocess

async def modal_folder_button(page, message: str, file_path: str = None):
    # Expose a Python binding so JS can call it
    async def open_folder_binding(source, fpath):
        folder = os.path.dirname(fpath)
        subprocess.Popen(f'explorer "{folder}"')
        return True

    try:
        await page.expose_binding("openFolderFromPython", open_folder_binding)
    except Exception as e:
        if "has been already registered" not in str(e):
            raise

    # Inject the modal
    await page.evaluate(
        """({customMessage, filePath}) => {
            return new Promise((resolve) => {
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
                modalContent.style.maxWidth = '400px';

                const messageDiv = document.createElement('div');
                messageDiv.innerHTML = customMessage;
                messageDiv.style.marginBottom = '20px';
                modalContent.appendChild(messageDiv);

                const buttonsContainer = document.createElement('div');
                buttonsContainer.style.display = 'flex';
                buttonsContainer.style.justifyContent = 'center';
                buttonsContainer.style.gap = '15px';

                // CONTINUE button
                const continueButton = document.createElement('button');
                continueButton.innerHTML = '<b>CONTINUE</b>';
                continueButton.style.padding = '10px 20px';
                continueButton.style.backgroundColor = '#266ab5';
                continueButton.style.color = 'white';
                continueButton.style.border = 'none';
                continueButton.style.borderRadius = '8px';
                continueButton.style.cursor = 'pointer';
                continueButton.style.width = '120px';
                continueButton.onclick = () => {
                    modalBackground.remove();
                    resolve("CONTINUE");
                };

                // OPEN FOLDER button
                const openButton = document.createElement('button');
                openButton.innerHTML = '<b>OPEN FOLDER</b>';
                openButton.style.padding = '10px 20px';
                openButton.style.backgroundColor = '#15db06';
                openButton.style.color = 'white';
                openButton.style.border = 'none';
                openButton.style.borderRadius = '8px';
                openButton.style.cursor = 'pointer';
                openButton.style.width = '150px';
                openButton.onclick = () => {
                    if (filePath) {
                        window.openFolderFromPython(filePath);
                    }
                };

                buttonsContainer.appendChild(openButton);
                buttonsContainer.appendChild(continueButton);
                modalContent.appendChild(buttonsContainer);
                modalBackground.appendChild(modalContent);
                document.body.appendChild(modalBackground);
            });
        }""",
        {"customMessage": message, "filePath": file_path}
    )



if __name__ =="__main__":
    modal_folder_button()