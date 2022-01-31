$(document).ready(function () {
	var current_user;
	$.get('/api/user/me', function (response) {
		console.log(response);
		current_user = response.name;
		$('#profile').text(`Welcome ${current_user}`);
		document.cookie = `current_user_name=${current_user}`;
	});

	fetch('/api/user/me')
		.then(response => {
			if (!response.ok) {
				throw new Error(response.statusText);
			}

			return response.json();
		})
		.then(response => {
			console.log(response);
			current_user = response.name;
			$('#profile').text(`Welcome ${current_user}`);
			document.cookie = `current_user_name=${current_user}`;
		})
		.catch(err => {
			console.log(err);
			alert(`Couldn't verify identy! Please Signin Again`);
			window.location.href = '/';
		});

	var ws = new WebSocket(`ws://${window.location.host}/ws/feed`);
	ws.onmessage = function (event) {
		console.log(`Web Socket: ${document.cookie}`);
		var parent = $('#messages');
		var data = JSON.parse(event.data);
		var sender = data['user'];
		if (sender == current_user) sender = 'You';

		var message = data['message'];
		var content = `<p class="feed">
				<strong class="feed-user"> ${sender} </strong>
				<span class="feed-message"> ${message} </span>
			</p>`;
		parent.append(content);
	};

	$('#chat-form').on('submit', function (e) {
		e.preventDefault();
		var message = $('input').val();
		if (message) {
			data = {
				user: current_user,
				message: message,
			};

			ws.send(JSON.stringify(data));

			$('input').val('');
		}
	});

	$('.logout-button').click(function () {
		fetch('/api/auth/logout', { method: 'POST' })
			.then(response => {
				if (!response.ok) {
					throw new Error(response.statusText);
				}

				return response.json();
			})
			.then(response => {
				console.log('Logout Successfull ............');
				alert('Logout Success');
				window.location.href = '/';
			})
			.catch(err => console.log(err));
	});
});
