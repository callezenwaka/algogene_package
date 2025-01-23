// Clipboard functionality
document.addEventListener('DOMContentLoaded', function() {
    const commands = document.querySelectorAll('.command');
    
    commands.forEach(command => {
        const copyButton = command.querySelector('.copy-button');
        const commandText = command.getAttribute('data-command');

        copyButton.addEventListener('click', async (e) => {
            e.stopPropagation(); // Prevent command div click
            try {
                await navigator.clipboard.writeText(commandText);
                copyButton.textContent = 'Copied!';
                setTimeout(() => {
                    copyButton.textContent = 'Copy';
                }, 2000);
            } catch (err) {
                console.error('Failed to copy:', err);
            }
        });

        // Make the entire command div clickable
        command.addEventListener('click', async () => {
            try {
                await navigator.clipboard.writeText(commandText);
                const button = command.querySelector('.copy-button');
                button.textContent = 'Copied!';
                setTimeout(() => {
                    button.textContent = 'Copy';
                }, 2000);
            } catch (err) {
                console.error('Failed to copy:', err);
            }
        });
    });
});

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
      alert('Copied!');
    }).catch(err => {
      console.error('Failed to copy: ', err);
    });
  }