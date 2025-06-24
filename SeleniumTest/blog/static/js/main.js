document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.btn-edit').forEach(button => {
        button.addEventListener('click', () => {
            const postId = button.dataset.postId;
            const postDiv = document.getElementById(`post-${postId}`);
            const titleEl = postDiv.querySelector('.post-title');
            const contentEl = postDiv.querySelector('.post-content');
            const deleteForm = document.querySelector(`form[data-post-id="${postId}"]`);

            console.log('postDiv:', postDiv);
            console.log('contentEl:', contentEl);
            console.log('deleteForm:', deleteForm);


            titleEl.style.display = 'none';
            contentEl.style.display = 'none';
            button.style.display = 'none';
            deleteForm.style.display = 'none';


            const form = document.createElement('form');
            form.setAttribute('data-testid', 'form-edit-post');
            form.innerHTML = `
                <input type="text" name="title" value="${titleEl.textContent}" required />
                <textarea name="content" required>${contentEl.textContent.trim()}</textarea>
                <button type="submit" data-testid="button-save-post">Save</button>
                <button type="button" data-testid="button-cancel-edit">Cancel</button>
            `;

            postDiv.appendChild(form);


            form.querySelector('[data-testid="button-cancel-edit"]').addEventListener('click', () => {
                form.remove();
                titleEl.style.display = '';
                contentEl.style.display = '';
                button.style.display = '';
                deleteForm.style.display = 'inline-block';
            });


            form.addEventListener('submit', e => {
                e.preventDefault();

                const formData = new FormData(form);
                fetch(`/posts/${postId}/edit_ajax/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                    },
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {

                        titleEl.textContent = data.post.title;
                        contentEl.textContent = data.post.content;

                        form.remove();
                        titleEl.style.display = '';
                        contentEl.style.display = '';
                        button.style.display = '';
                    } else {
                        alert('Error saving post: ' + data.error);
                    }
                })
                .catch(() => alert('Error communicating with server.'));
            });
        });
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


document.addEventListener('DOMContentLoaded', () => {
  const dropdownToggle = document.querySelector('.dropdown-toggle');
  const dropdownMenu = document.querySelector('.dropdown-menu');

  if (dropdownToggle && dropdownMenu) {
    dropdownToggle.addEventListener('click', () => {
      dropdownMenu.classList.toggle('show');
    });

    document.addEventListener('click', (event) => {
      if (!dropdownToggle.contains(event.target) && !dropdownMenu.contains(event.target)) {
        dropdownMenu.classList.remove('show');
      }
    });
  }
});