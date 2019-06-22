<!DOCTYPE html>
<html>
<head>
	<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css">

	<title>{{title or 'No title'}}</title>
	<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
</head>
<body class="grey darken-4 white-text">
	<nav class="grey darken-3" style="vertical-align: middle">
		<!--a href="/" class="brand-logo amber-text"><i class="amber-text material-icons" style="margin-left:15px">home</i></a-->
		<div class="nav-wrapper container">
			<form id="searchForm">
				<div class="input-field">
					<input id="search" type="search" placeholder="Search YouTube" required>
					<label class="label-icon" for="search"><i class="material-icons">search</i></label>
					<i class="material-icons">close</i>
				</div>
			</form>
		</div>
	</nav>

	<div class="container">
		{{!base}}
	</div>

	<script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
	<script src="https://code.jquery.com/jquery-3.4.1.min.js" integrity="sha256-CSXorXvZcTkaix6Yvo6HppcZGetbYMGWSFlBw8HfCJo=" crossorigin="anonymous"></script>
	<script>
		$(document).ready(function() {
			$('#searchForm').submit(function(){
				var query = $('#search').val();
				$(this).attr('action', "/search/" + query);
			});
		});
	</script>
	<script>
		$('.collection-item').hover(
			function(){
				$(this).removeClass('darken-4')
				$(this).addClass('darken-3')
			},
			function(){
				$(this).removeClass('darken-3')
				$(this).addClass('darken-4')
			}
		);
	</script>
</body>
</html>
