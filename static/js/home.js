$(document).ready(function () {
	$('#login-form').on('submit', function (e) {
		e.preventDefault();
		var user_email = $('#user_email').val();
		var user_password = $('#user_password').val();

		if (user_email && user_password) {
			var formBody = new URLSearchParams();

			formBody.append('username', user_email);
			formBody.append('password', user_password);

			console.log(formBody.values());

			fetch('/api/auth/login', {
				method: 'POST',
				body: formBody,
				headers: {
					'Content-Type': 'application/x-www-form-urlencoded',
					accept: 'application/json',
				},
			})
				.then(response => {
					if (!response.ok) {
						throw new Error(response.status);
					}

					return response.json();
				})
				.then(response => {
					console.log(response);
					window.location.href = '/feed';
				})
				.catch(err => {
					console.log('Message from Error');
					console.log(err);
					alert('Wrong Credentials');
				});
		}
	});

	$('#signup-form').on('submit', function (e) {
		console.log('Submissions Called');
		e.preventDefault();
		var user_email = $('#s_user_email').val();
		var user_password = $('#s_user_password').val();
		var user_name = $('#s_user_name').val();

		if (user_email && user_password) {
			console.log(user_email, user_password);

			const data = {
				email: user_email,
				password: user_password,
				name: user_name,
			};

			fetch('/api/auth/register', {
				method: 'POST',
				body: JSON.stringify(data),
				headers: {
					'Content-Type': 'application/json',
				},
			})
				.then(response => {
					if (!response.ok) {
						throw new Error(response.status);
					}

					return response.json();
				})
				.then(response => {
					console.log(response);
					alert('User Register Sucessfully');
				})
				.catch(err => console.log(err));
		}
	});
});
