% rebase('templates/base.tpl', title='Results')
<ul class="collection with-header">
	<li class="collection-header"><h4>{{header}}</h4>{{subheader}}</li>
	%for vid in videos:
		<li class="collection-item"><div>
			<img src="https://img.youtube.com/vi/{{vid[0]}}/default.jpg">{{vid[1]}}
			<a href="/add/{{vid[0]}}/{{vid[2]}}" class="secondary-content"><i class="material-icons">playlist_add</i></a>
		</div></li>
	%end
</ul>
